"""Provides a frontend class for using the erasure simulation models."""

from erado import (
    models,
    util,
    fidelity,
)

import qiskit.providers

import pydantic
import numpy as np

from collections import Counter
from multiprocessing.managers import SharedMemoryManager


class ErasureSimResults(pydantic.BaseModel):
    """Data structure of the results from an `ErasureSimFrontend` run."""
    shots: int
    n_accepted: int
    n_rejected: int
    rejection_rate: float
    circuit_depth: int
    n_erasable_gates: int
    counts: Counter[models.CircuitState]
    fidelity: util.NPPydantic[util.NPVector[np.float64]]

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class ErasureSimFrontend(util.MultiprocessingRNG):
    """Erasure simulation frontend supporting any `ErasureModel`.

    This utility adds logic for postselection on end-of-line (EOL) erasure checks, as well as noise
    on these checks in the form of false positive/negative rates.

    See `example_ErasureSimFrontend` for example usage.
    """
    def __init__(
            self,
            model: models.ErasureModel,
            noisy_checks: bool = False,
            false_positive_rate: float = 0,
            false_negative_rate: float = 0
        ):
        """Construct an `ErasureSimFrontend`.

        Args:
            model: Configured `ErasureModel` to use for simulation.
            noisy_checks: If true, EOL erasure checks are subject to noise.
            false_positive_rate: Probability that negative erasure checks are flipped.
            false_negative_rate: Probability that positive erasure checks are flipped.
        """
        self._model = model
        self._noisy_checks = noisy_checks
        self._false_positive_rate = false_positive_rate
        self._false_negative_rate = false_negative_rate

    @property
    def model(self) -> models.ErasureModel:
        """`ErasureModel` used to construct this `ErasureSimFrontend`."""
        return self._model

    @property
    def noisy_checks(self) -> bool:
        """If true, EOL erasure checks are subject to noise."""
        return self._noisy_checks

    @property
    def false_positive_rate(self) -> float:
        """Probability that negative erasure checks are flipped."""
        return self._false_positive_rate

    @property
    def false_negative_rate(self) -> float:
        """Probability that positive erasure checks are flipped."""
        return self._false_negative_rate

    @property
    def n_qubits(self) -> int:
        """Number of qubits in the quantum circuit."""
        return self.model.circuit.num_qubits

    def _bernoulli_bitstring(self, p: float) -> int:
        """Generate an integer with each bit set with probability p."""
        bits = self._rng.binomial(1, p, self.n_qubits)
        return int("".join(str(bit) for bit in bits), 2)

    def _add_check_noise(self, state: models.CircuitState) -> models.CircuitState:
        # Represent erasure state as bitstring
        x = int(state.erasure, 2)

        # Generate random false pos/neg bit-flip noise
        e_false_neg_raw = self._bernoulli_bitstring(self.false_negative_rate)
        e_false_pos_raw = self._bernoulli_bitstring(self.false_positive_rate)

        # Mask false pos/neg noise to positive/negative events in x
        # (note the mask-subtraction pattern as a 'true' bitwise NOT for n_qubits)
        e_false_neg = x & e_false_neg_raw
        e_false_pos = ((1 << self.n_qubits) - 1 - x) & e_false_pos_raw

        # Apply the noise (sum modulo 2) and convert back to string
        x_noisy = x ^ e_false_neg ^ e_false_pos
        x_noisy_str = format(x_noisy, f"0{self.n_qubits}b")

        return models.CircuitState(erasure=x_noisy_str, measure=state.measure)

    def _run_once(
            self,
            backend: qiskit.providers.BackendV2,
            shots: int,
            fidelity_functor: fidelity.FidelityFunctor | None,
            model_kwargs: dict[str, object],
        ) -> Counter[models.CircuitState]:
        callbacks: list[models.ShotCallback] = []
        if fidelity_functor is not None:
            callbacks.append(fidelity_functor)

        counts = self.model.run(backend, shots, callbacks, **model_kwargs)

        if self.noisy_checks:
            if fidelity_functor is not None:
                # If using FidelityFunctor, use it as the source of truth for all observed states.
                # Also, we must send the noise-inflicted states back into the generator.
                counts = Counter[models.CircuitState]()
                results = fidelity_functor.results()
                for _, state in results:
                    noisy_state = self._add_check_noise(state)
                    counts[noisy_state] += 1
                    results.send(noisy_state)

            else:
                counts = Counter((self._add_check_noise(elt) for elt in counts.elements()))

        return counts

    def _count_rejected(self, counts: Counter[models.CircuitState]) -> int:
        return sum((count
                    for state, count in counts.items()
                    if state.erasure != "0"*self.n_qubits))

    def run(
            self,
            backend: qiskit.providers.BackendV2,
            shots: int,
            postselect: bool = False,
            get_fidelities: bool = False,
            **kwargs: object,
        ) -> ErasureSimResults:
        """Execute the simulation on a given backend for some number of shots.

        This uses the `run` method on the `model` to generate the target number of shots.
        Postselection can be enabled by setting `postselect` to `True`, in which case any shots
        where any qubits were erased (as per potentially-noisy end-of-line checks) are rejected.
        Further shots are generated via the `model` until the target number of shots are accepted.

        The calculation of per-shot fidelities can be enabled with `get_fidelities`. If enabled,
        there must exist a snapshot gate of the form `save_x` (i.e. one of the instructions
        specified in `erado.models.SNAPSHOT_GATES`) saving the state with the label
        `erado.fidelity.STATE_LABEL`.

        Args:
            backend: Circuit simulator backend.
            shots: Target number of shots.
            postselect: If true, postselect on negative erasure checks until the target number of
                shots.
            get_fidelities: If true, calculate and store per-shot fidelities.
            **kwargs: Additional keyword arguments passed onto `ErasureModel.run`.

        Raises:
            ValueError: If `get_fidelities` is true but the circuit has no appropriate `save_x`.
            RuntimeError: If the resultant number of shots does not equal the target for some reason.

        Returns:
            Data structure of results and statistics from the simulation.
        """
        with SharedMemoryManager() as smm:
            # A new FidelityFunctor is needed for each postselection round
            # (as they are effectively distinct simulations, each one unaware of the last)
            fidelity_functors = list[fidelity.FidelityFunctor]()

            fidelity_functor = None
            if get_fidelities:
                if not any((gate.name in models.SNAPSHOT_GATES and gate.label == fidelity.STATE_LABEL
                            for gate in self.model.circuit.data)):
                    raise ValueError(f"Cannot get fidelities without a snapshot gate labelled {fidelity.STATE_LABEL}.")

                fidelity_functors.append(fidelity_functor := fidelity.FidelityFunctor(shots, self.model.circuit, smm))

            counts = self._run_once(backend, shots, fidelity_functor, kwargs)
            total_shots = shots
            n_rejected = self._count_rejected(counts)

            if postselect:
                n_remaining = n_rejected
                while n_remaining > 0:
                    if get_fidelities:
                        fidelity_functors.append(fidelity_functor := fidelity.FidelityFunctor(n_remaining, self.model.circuit, smm))

                    counts.update(self._run_once(backend, n_remaining, fidelity_functor, kwargs))
                    total_shots += n_remaining
                    n_rejected = self._count_rejected(counts)
                    n_remaining = shots - (total_shots - n_rejected)
                n_accepted = total_shots - n_rejected
            else:
                n_accepted = total_shots

            if n_accepted != shots:
                raise RuntimeError("The requested number of shots was exceeded or not reached.")

            fidelity_array = np.array([])
            if get_fidelities:
                if postselect:
                    # Aggregate accepted shots from all postselection rounds
                    generator = (fidelity
                                 for ff in fidelity_functors
                                 for fidelity, state in ff.results()
                                 if "1" not in state.erasure)
                else:
                    generator = (fidelity
                                 for ff in fidelity_functors
                                 for fidelity, _ in ff.results())

                fidelity_array = np.fromiter(generator,
                                             dtype=np.float64,
                                             count=shots)

        return ErasureSimResults(
            shots=total_shots,
            n_accepted=n_accepted,
            n_rejected=n_rejected,
            rejection_rate=n_rejected / total_shots,
            circuit_depth=self.model.circuit.depth(),
            n_erasable_gates=self.model.n_erasable_gates,
            counts=counts,
            fidelity=fidelity_array,
        )
