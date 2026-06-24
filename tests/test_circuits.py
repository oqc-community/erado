"""Tests the factories and utilities in :mod:`erado.circuits`."""

import pytest
import qiskit
import qiskit_aer

from erado import circuits


@pytest.fixture
def qft_circuit(n: int) -> qiskit.QuantumCircuit:
    """Fixture providing a linear QFT circuit with `n` qubits transpiled to [rz, sx, cx]."""
    circuit = circuits.qft_linear(n)

    basis_gates_1Q = ["rz", "sx"]
    basis_gates_2Q = ["cx"]
    basis_gates = ["id"] + basis_gates_1Q + basis_gates_2Q
    noise_model = qiskit_aer.noise.NoiseModel(basis_gates=basis_gates)
    backend = qiskit_aer.AerSimulator(method="statevector", device="GPU", noise_model=noise_model)
    pass_manager = qiskit.generate_preset_pass_manager(backend=backend)
    circuit_transpiled = pass_manager.run(circuit)

    return circuit_transpiled


@pytest.mark.parametrize("n", range(2, 17))
def test_qft_linear(qft_circuit: qiskit.QuantumCircuit, n: int):
    """Test that :func:`erado.circuits.qft_linear` provides a circuit of length :math:`3n^2-2n+2`."""
    assert isinstance(qft_circuit, qiskit.QuantumCircuit)
    assert len(qft_circuit.data) == 3*n**2 - 2*n + 2


@pytest.mark.parametrize("n", range(2, 17))
def test_pad_idling_return_type(qft_circuit: qiskit.QuantumCircuit):
    """Test that :func:`erado.circuits.pad_idling` returns a :class:`qiskit.circuit.QuantumCircuit`."""
    circuit_idling = circuits.pad_idling(qft_circuit)
    assert isinstance(circuit_idling, qiskit.QuantumCircuit)


def get_sequence(
        circuit: qiskit.QuantumCircuit,
        start: int,
        stop: int,
    ) -> tuple[list[str], list[int]]:
    """Retrieve the names and qargs of circuit gates in a specified range."""
    return (
        [g.name for g in circuit.data[start:stop]],
        [g.qubits[0]._index for g in circuit.data[start:stop]],
    )


@pytest.mark.parametrize("n", [3])
def test_pad_idling_expected_sequences(qft_circuit: qiskit.QuantumCircuit):
    """Test that :func:`erado.circuits.pad_idling` with default behaviour inserts the expected idle sequences."""
    circuit_idling = circuits.pad_idling(qft_circuit)

    # 2 I in idle period of 2
    name, qargs = get_sequence(circuit_idling, 30, 34)
    assert name == ["rz"] + ["id"]*2 + ["rz"]
    assert qargs == [1] + [2]*2 + [2]

    # 2 I in idle period of 3
    name, qargs = get_sequence(circuit_idling, 7, 11)
    assert name == ["id"] + ["id"]*2 + ["rz"]
    assert qargs == [0] + [1]*2 + [2]

    # 8 I in idle period of 8
    name, qargs = get_sequence(circuit_idling, 0, 9)
    assert name == ["id"]*8 + ["id"]
    assert qargs == [0]*8 + [1]


def test_pad_idling_max_length():
    """Test that :func:`erado.circuits.pad_idling` correctly inserts the `max_idle_length`."""
    circuit = qiskit.QuantumCircuit(2)
    for _ in range(20):
        circuit.x(1)
    circuit.measure_all()

    circuit_idling = circuits.pad_idling(circuit)

    name, qargs = get_sequence(circuit_idling, 0, 15)
    assert name == ["id"]*14 + ["x"]
    assert qargs == [0]*14 + [1]
