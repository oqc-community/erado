from erado.models import CircuitState

import pytest


def test_serialise():
    num_qubits = 5
    state = CircuitState(erasure="0"*num_qubits, measure="1"*num_qubits)
    state_str = state.model_dump_json()
    assert state_str == "\"00000,11111\""


@pytest.mark.parametrize("state_str,expected", [
    (f"\"{"0"*5},{"1"*5}\"", ("0"*5, "1"*5)),  # Measure all qubits
    (f"\"{"0"*5},{"1"*2}\"", ("0"*5, "1"*2))   # Measure only some qubits
])
def test_deserialise(state_str: str, expected: tuple[str, str]):
    state = CircuitState.model_validate_json(state_str)
    assert isinstance(state, CircuitState)
    assert state.erasure == expected[0]
    assert state.measure == expected[1]


@pytest.mark.parametrize("state_str,expected", [
    ("0"*5 + "1"*5, ("0"*5, "1"*5)),    # Measure all qubits
    ("0 "*5 + "1 "*5, ("0"*5, "1"*5)),  # Arbitrary whitespace from qiskit
    ("0"*5 + "1"*2, ("0"*5, "1"*2))     # Measure only some qubits
])
def test_from_string(state_str: str, expected: tuple[str, str]):
    state = CircuitState.from_string(state_str)
    assert isinstance(state, CircuitState)
    assert state.erasure == expected[0]
    assert state.measure == expected[1]
