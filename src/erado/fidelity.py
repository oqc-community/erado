from erado.models import (
    CircuitState,
    postselect_counts
)
from erado.util import NPVector

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

import numpy as np

from collections import Counter


def calculate_pdf(circuit: QuantumCircuit) -> NPVector[np.float64]:
    circuit_pure = circuit.remove_final_measurements(inplace=False)
    if circuit_pure is None:
        raise RuntimeError("Qiskit's remove_final_measurements did not return a circuit as requested.")

    psi = Statevector(circuit_pure)
    pdf = np.abs(psi)**2
    return pdf


def calculate_fidelity(counts: Counter[CircuitState], circuit: QuantumCircuit) -> float:
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
