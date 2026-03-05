"""Provides a selection of quantum circuits for benchmarking."""

import qiskit
from qiskit import synthesis


def ghz(n: int) -> qiskit.QuantumCircuit:
    """Greenberger-Horne-Zeilinger (GHZ) state preparation.

    Args:
        n: Number of qubits.

    Returns:
        Qiskit quantum circuit.
    """
    qc = qiskit.QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)

    return qc


def qft_full(n: int) -> qiskit.QuantumCircuit:
    """Quantum Fourier transform (QFT) on all-to-all connectivity.

    This directly invokes :func:`qiskit.synthesis.synth_qft_full`.

    Args:
        n: Number of qubits.

    Returns:
        Qiskit quantum circuit.
    """
    return synthesis.synth_qft_full(n)


def qft_linear(n: int) -> qiskit.QuantumCircuit:
    """Quantum Fourier transform (QFT) on linear connectivity.

    This directly invokes :func:`qiskit.synthesis.synth_qft_line`, which uses a construction based on
    Fowler et al. 2014 (https://arxiv.org/abs/quant-ph/0402196).

    Args:
        n: Number of qubits.

    Returns:
        Qiskit quantum circuit.
    """
    # TODO: linear nearest-neighbour QFT compiled in the parityQC method (best QFT compilation to date)
    # https://arxiv.org/pdf/2501.14020
    return synthesis.synth_qft_line(n)
