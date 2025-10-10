from erado.models import ErasureModel
from erado.util import MultiprocessingRNG, standardise_counts

from qiskit.providers import BackendV2 as Backend

from pydantic import BaseModel

from dataclasses import dataclass
from collections import Counter


class ErasureSimFrontendResults(BaseModel):
    counts: Counter[tuple[str, str]]
    shots: int
    n_rejected: int
    rejection_rate: float
    circuit_depth: int
    n_erasable_gates: int


class ErasureSimFrontend(MultiprocessingRNG):
    """
    Erasure simulation frontend supporting any `ErasureModel`.

    This utility adds logic for postselection on end-of-line erasure checks, as well as noise
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
        self._model = model
        self._noisy_checks = noisy_checks
        self._false_positive_rate = false_positive_rate
        self._false_negative_rate = false_negative_rate

    @property
    def model(self): return self._model

    @property
    def noisy_checks(self): return self._noisy_checks

    @property
    def false_positive_rate(self): return self._false_positive_rate

    @property
    def false_negative_rate(self): return self._false_negative_rate

    @property
    def num_qubits(self) -> int: return self.model.circuit.num_qubits

    def _bernoulli_bitstring(self, p: float) -> int:
        """Generate an integer with each bit set with probability p."""
        bits = self._rng.binomial(1, p, self.num_qubits)
        return int("".join(str(bit) for bit in bits), 2)

    def _add_check_noise(self, state: tuple[str, str]) -> tuple[str, str]:
        # Represent erasure state as bitstring
        x = int(state[0], 2)

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

        return x_noisy_str, state[1]

    def _run_once(self, backend: Backend, shots: int) -> Counter[tuple[str, str]]:
        counts = self.model.run(backend, shots)
        counts = standardise_counts(counts)

        if self.noisy_checks:
            counts = Counter((self._add_check_noise(elt) for elt in counts.elements()))

        return counts

    def _count_rejected(self, counts) -> int:
        return sum((count
                    for state, count in counts.items()
                    if state[0] != "0"*self.num_qubits))

    def run(self, backend: Backend, shots: int, postselect: bool = False) -> ErasureSimFrontendResults:
        """
        Execute the simulation on a given backend for some number of shots.

        This uses the `run` method on the `model` to generate the target number of shots.
        Postselection can be enabled by setting `postselect` to `True`, in which case any shots
        where any qubits were erased (as per potentially-noisy end-of-line checks) are rejected.
        Further shots are generated via the `model` until the target number of shots are accepted.
        """
        counts = self._run_once(backend, shots)
        total_shots = shots
        n_rejected = self._count_rejected(counts)

        if postselect:
            n_remaining = n_rejected
            while n_remaining > 0:
                counts.update(self._run_once(backend, n_remaining))
                total_shots += n_remaining
                n_rejected = self._count_rejected(counts)
                n_remaining = shots - (total_shots - n_rejected)

        if total_shots - n_rejected != shots:
            raise RuntimeError("The requested number of shots was exceeded or not reached.")

        return ErasureSimFrontendResults(
            counts=counts,
            shots=total_shots,
            n_rejected=n_rejected,
            rejection_rate=n_rejected / total_shots,
            circuit_depth=self.model.circuit.depth(),
            n_erasable_gates=self.model.n_erasable_gates
        )
