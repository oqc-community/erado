"""Provides a selection of quantum circuits for benchmarking."""

from qiskit import QuantumCircuit


def ghz_circuit(n: int) -> QuantumCircuit:
    """Greenberger-Horne-Zeilinger (GHZ) state preparation.

    Args:
        n: Number of qubits.

    Returns:
        A new Qiskit quantum circuit.
    """
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)

    return qc
