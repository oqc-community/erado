"""Provides a frontend class for using the erasure simulation models."""

from erado.models import (
    ErasureModel,
    CircuitState,
    ShotCallback,
)
from erado.util import (
    MultiprocessingRNG,
    NPVector,
    NPPydantic,
)
from erado.fidelity import FidelityFunctor

from qiskit.providers import BackendV2 as Backend

import pydantic
import numpy as np

from collections import Counter


class ErasureSimResults(pydantic.BaseModel):
    """Data structure of the results from an `ErasureSimFrontend` run."""
    counts: Counter[CircuitState]
    shots: int
    n_rejected: int
    rejection_rate: float
    circuit_depth: int
    n_erasable_gates: int
    fidelity: NPPydantic[NPVector[np.float64]]

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class ErasureSimFrontend(MultiprocessingRNG):
    """Erasure simulation frontend supporting any `ErasureModel`.

    This utility adds logic for postselection on end-of-line (EOL) erasure checks, as well as noise
    on these checks in the form of false positive/negative rates.

    See `example_ErasureSimFrontend` for example usage.
    """
    def __init__(
            self,
            model: ErasureModel,
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
    def model(self) -> ErasureModel:
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

    # TODO: we've used n_{object} elsewhere... change to n_qubits?
    @property
    def num_qubits(self) -> int:
        """Number of qubits in the quantum circuit."""
        return self.model.circuit.num_qubits

    def _bernoulli_bitstring(self, p: float) -> int:
        """Generate an integer with each bit set with probability p."""
        bits = self._rng.binomial(1, p, self.num_qubits)
        return int("".join(str(bit) for bit in bits), 2)

    def _add_check_noise(self, state: CircuitState) -> CircuitState:
        # Represent erasure state as bitstring
        x = int(state.erasure, 2)

        # Generate random false pos/neg bit-flip noise
        e_false_neg_raw = self._bernoulli_bitstring(self.false_negative_rate)
        e_false_pos_raw = self._bernoulli_bitstring(self.false_positive_rate)

        # Mask false pos/neg noise to positive/negative events in x
        # (note the mask-subtraction pattern as a 'true' bitwise NOT for num_qubits)
        e_false_neg = x & e_false_neg_raw
        e_false_pos = ((1 << self.num_qubits) - 1 - x) & e_false_pos_raw

        # Apply the noise (sum modulo 2) and convert back to string
        x_noisy = x ^ e_false_neg ^ e_false_pos
        x_noisy_str = format(x_noisy, f"0{self.num_qubits}b")

        return CircuitState(erasure=x_noisy_str, measure=state.measure)

    def _run_once(
            self,
            backend: Backend,
            shots: int,
            callbacks: list[ShotCallback],
            fidelity_functor: FidelityFunctor | None,
        ) -> Counter[CircuitState]:
        if fidelity_functor is not None:
            fidelity_functor.new_round()

        counts = self.model.run(backend, shots, callbacks, multiprocess=False)
        # TODO: multiprocess=False is jsut temporary here!!! Support kwargs properly?

        if self.noisy_checks:
            if fidelity_functor is not None:
                counts = Counter[CircuitState]()
                for result in fidelity_functor.results_round():
                    result.state = self._add_check_noise(result.state)
                    counts[result.state] += 1
            else:
                counts = Counter((self._add_check_noise(elt) for elt in counts.elements()))

        return counts

    def _count_rejected(self, counts: Counter[CircuitState]) -> int:
        return sum((count
                    for state, count in counts.items()
                    if state.erasure != "0"*self.num_qubits))

    def run(
            self,
            backend: Backend,
            shots: int,
            postselect: bool = False,
            get_fidelities: bool = True,
        ) -> ErasureSimResults:
        """Execute the simulation on a given backend for some number of shots.

        This uses the `run` method on the `model` to generate the target number of shots.
        Postselection can be enabled by setting `postselect` to `True`, in which case any shots
        where any qubits were erased (as per potentially-noisy end-of-line checks) are rejected.
        Further shots are generated via the `model` until the target number of shots are accepted.

        Args:
            backend: Circuit simulator backend.
            shots: Target number of shots.
            postselect: If true, postselect on negative erasure checks until the target number of
                shots.

        Raises:
            RuntimeError: If the resultant number of shots does not equal the target for some reason.

        Returns:
            Data structure of results and statistics from the simulation.
        """
        callbacks = list[ShotCallback]()

        fidelity_functor = None
        if get_fidelities:
            callbacks.append(fidelity_functor := FidelityFunctor())
            # TODO: should fidelity_functor be refactored to a private field?

        counts = self._run_once(backend, shots, callbacks, fidelity_functor)
        total_shots = shots
        n_rejected = self._count_rejected(counts)

        if postselect:
            n_remaining = n_rejected
            while n_remaining > 0:
                counts.update(self._run_once(backend, n_remaining, callbacks, fidelity_functor))
                total_shots += n_remaining
                n_rejected = self._count_rejected(counts)
                n_remaining = shots - (total_shots - n_rejected)

        if total_shots - n_rejected != shots:
            raise RuntimeError("The requested number of shots was exceeded or not reached.")

        fidelity_array = np.array([])
        if fidelity_functor is not None:
            if postselect:
                generator = (result.fidelity for result in fidelity_functor.results()
                             if "1" not in result.state.erasure)
            else:
                generator = (result.fidelity for result in fidelity_functor.results())

            fidelity_array = np.fromiter(generator,
                                         dtype=np.float64,
                                         count=shots)

        return ErasureSimResults(
            counts=counts,
            shots=total_shots,
            n_rejected=n_rejected,
            rejection_rate=n_rejected / total_shots,
            circuit_depth=self.model.circuit.depth(),
            n_erasable_gates=self.model.n_erasable_gates,
            fidelity=fidelity_array,
        )
