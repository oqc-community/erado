# TODO: Support multiprocessing (via shared memory or similar).
# TODO: Don't forget to update all signatures/docstrings etc.

from erado.models import (
    CircuitState,
    ShotInfo,
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
        if circuit_pure.data[i].operation.name in ["save_statevector", "save_density_matrix"]:
            del circuit_pure.data[i]

    return Statevector(circuit_pure)


STATE_LABEL = "final_state"


class FidelityFunctor:
    @dataclass
    class Result:
        state: CircuitState
        fidelity: float

    def __init__(self, circuit: QuantumCircuit | None):
        self._circuit_sv = calculate_statevector(circuit) if circuit is not None else None
        self._results = list[self.Result]()
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
            self._results.append(self.Result(info.state, fid))
        except KeyError:
            _logger.error(f"No {STATE_LABEL} found in this shot (state: {info.state}); using NaN for fidelity.")
            self._results.append(self.Result(info.state, np.nan))

    def new_round(self) -> None:
        self._round_size = 0

    def _results_generator(self, start: int, stop: int) -> Generator[Result]:
        for i in range(start, stop):
            yield self._results[i]

    def results(self) -> Generator[Result]:
        yield from self._results_generator(
            0, len(self._results)
        )

    def results_round(self) -> Generator[Result]:
        yield from self._results_generator(
            len(self._results) - self._round_size, len(self._results)
        )
