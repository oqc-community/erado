from erado.models import (
    CircuitState,
    postselect_counts,
    ShotInfo,
)
from erado.util import NPVector

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

import numpy as np

from collections import Counter
from collections.abc import Generator
from dataclasses import dataclass
import logging


_logger = logging.getLogger(__name__)


def calculate_pdf(circuit: QuantumCircuit) -> NPVector[np.float64]:
    # Remove any final measurements (we want the final state of the circuit before observation)
    circuit_pure = circuit.remove_final_measurements(inplace=False)
    if circuit_pure is None:
        raise RuntimeError("Qiskit's remove_final_measurements did not return a circuit as requested.")

    # Also remove any save_statevector calls (else constructing the `Statevector` will fail)
    for i in reversed(range(len(circuit_pure.data))):
        if circuit_pure.data[i].operation.name == "save_statevector":
            del circuit_pure.data[i]

    psi = Statevector(circuit_pure)
    pdf = np.abs(psi)**2
    return pdf


def calculate_fidelity_old(counts: Counter[CircuitState], circuit: QuantumCircuit) -> float:
    # Calculate the exact non-noisy probability density function
    pdf_ideal = calculate_pdf(circuit)

    # Calculate the empirical noisy probability density function
    counts_noisy = postselect_counts(counts)
    shots = counts_noisy.total()
    n = circuit.num_qubits
    states = (format(i, f"0{n}b") for i in range(2**n))
    pdf_noisy = np.fromiter((counts_noisy[state] / shots
                             for state in states),
                            dtype=np.float64)

    # Calculate the fidelity (i.e. square of the Bhattacharyya coefficient)
    fidelity = np.inner(np.sqrt(pdf_ideal), np.sqrt(pdf_noisy))**2
    return fidelity


def calculate_fidelity(psi: Statevector, ideal: QuantumCircuit | Statevector | NPVector[np.float64]) -> float:
    # Calculate the exact non-noisy probability density function
    if isinstance(ideal, QuantumCircuit):
        pdf_ideal = calculate_pdf(ideal)
    elif isinstance(ideal, Statevector):
        pdf_ideal = np.abs(ideal)**2
    else:
        pdf_ideal = ideal

    # Calculate the noisy probability density function from this shot
    pdf_noisy = np.abs(psi)**2

    # Calculate the fidelity (i.e. square of the Bhattacharyya coefficient)
    fidelity = np.inner(np.sqrt(pdf_ideal), np.sqrt(pdf_noisy))**2
    return fidelity


class FidelityFunctor:
    @dataclass
    class Result:
        state: CircuitState
        fidelity: float

    def __init__(self, circuit: QuantumCircuit | None = None):
        self._pdf_ideal = calculate_pdf(circuit) if circuit is not None else None
        self._results = list[self.Result]()
        self._round_size: int = 0

    def __call__(self, info: ShotInfo) -> None:
        self._round_size += 1
        try:
            psi = info.result.data(0)["psi"][0]  # First instance of psi in first shot (there will only be one of each)
            fid = calculate_fidelity(
                psi,
                self._pdf_ideal if self._pdf_ideal is not None else info.model.circuit,
            )
            self._results.append(self.Result(info.state, fid))
        except KeyError:
            _logger.debug("No psi found in this shot! Using NaN.")  # TODO: is this because of erasure events?
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
