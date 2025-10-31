# TODO: Support multiprocessing (via shared memory or similar).
# TODO: Don't forget to update all signatures/docstrings etc.

from erado.models import (
    CircuitState,
    ShotInfo,
    SNAPSHOT_GATES,
)

from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Statevector,
    DensityMatrix,
    state_fidelity,
)

import numpy as np

from collections.abc import Generator
from dataclasses import dataclass
import logging


_logger = logging.getLogger(__name__)


def calculate_statevector(circuit: QuantumCircuit) -> Statevector:
    # Remove any final measurements (we want the final state of the circuit before observation)
    circuit_pure = circuit.remove_final_measurements(inplace=False)
    if circuit_pure is None:
        raise RuntimeError("Qiskit's remove_final_measurements did not return a circuit as requested.")

    # Also remove any snapshot calls (else constructing the `Statevector` will fail)
    for i in reversed(range(len(circuit_pure.data))):
        if circuit_pure.data[i].operation.name in SNAPSHOT_GATES:
            del circuit_pure.data[i]

    return Statevector(circuit_pure)


STATE_LABEL = "final_state"


@dataclass
class FidelityResult:
    state: CircuitState
    fidelity: float


class FidelityFunctor:
    def __init__(self, circuit: QuantumCircuit | None):
        self._circuit_sv = calculate_statevector(circuit) if circuit is not None else None
        self._results = list[FidelityResult]()
        self._round_size: int = 0

    def __call__(self, info: ShotInfo) -> None:
        self._round_size += 1
        try:
            # First instance of final_state in first shot (there will only be one of each)
            final_state: Statevector | DensityMatrix = info.result.data(0)[STATE_LABEL][0]
            fid = state_fidelity(
                final_state,
                self._circuit_sv if self._circuit_sv is not None else calculate_statevector(info.model.circuit)
            )
            self._results.append(FidelityResult(info.state, fid))
        except KeyError:
            _logger.error(f"No {STATE_LABEL} found in this shot (state: {info.state}); using NaN for fidelity.")
            self._results.append(FidelityResult(info.state, np.nan))

    def new_round(self) -> None:
        self._round_size = 0

    def _results_generator(self, start: int, stop: int) -> Generator[FidelityResult]:
        for i in range(start, stop):
            yield self._results[i]

    def results(self) -> Generator[FidelityResult]:
        yield from self._results_generator(
            0, len(self._results)
        )

    def results_round(self) -> Generator[FidelityResult]:
        yield from self._results_generator(
            len(self._results) - self._round_size, len(self._results)
        )
