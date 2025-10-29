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


def calculate_fidelity(psi: Statevector, circuit_ideal: QuantumCircuit) -> float:
    # Calculate the exact non-noisy probability density function
    pdf_ideal = calculate_pdf(circuit_ideal)

    # Calculate the noisy probability density function from this shot
    pdf_noisy = np.abs(psi)**2

    # Calculate the fidelity (i.e. square of the Bhattacharyya coefficient)
    fidelity = np.inner(np.sqrt(pdf_ideal), np.sqrt(pdf_noisy))**2
    return fidelity


class FidelityFunctor:
    def __init__(self):
        self.fidelities = list[tuple[str, float]]()

    def __call__(self, info: ShotInfo) -> None:
        try:
            psi = info.result.data(0)["psi"][0]  # First instance of psi in first shot (there will only be one of each)
            fid = calculate_fidelity(psi, info.model.circuit)
            self.fidelities.append((info.state.erasure, fid))
        except KeyError:
            _logger.debug("No psi found in this shot! Using NaN.")
            self.fidelities.append((info.state.erasure, np.nan))
