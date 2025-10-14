from erado.models import CircuitState

import pytest


N = 5
"""Number of qubits to use in these tests, unless otherwise specified."""


def test_serialise_str():
    """String representation should be the readable and compact version.

    This is invoked when serialising JSON from container objects, e.g. `ErasureSimFrontendResults`.
    """
    state = CircuitState(erasure="0"*N, measure="1"*N)
    state_str = str(state)
    assert state_str == "00000,11111"


def test_serialise_json():
    """If explicitly invoking JSON serialisation, it must instead be valid JSON."""
    state = CircuitState(erasure="0"*N, measure="1"*N)
    state_str = state.model_dump_json()
    assert state_str == "{\"erasure\":\"00000\",\"measure\":\"11111\"}"


@pytest.mark.parametrize("state_str,expected", [
    (f"\"{"0"*N},{"1"*N}\"", ("0"*N, "1"*N)),  # Measure all qubits
    (f"\"{"0"*N},{"1"*2}\"", ("0"*N, "1"*2))   # Measure only some qubits
])
def test_deserialise(state_str: str, expected: tuple[str, str]):
    state = CircuitState.model_validate_json(state_str)
    assert isinstance(state, CircuitState)
    assert state.erasure == expected[0]
    assert state.measure == expected[1]


@pytest.mark.parametrize("state_str,expected", [
    ("0"*N + "1"*N, ("0"*N, "1"*N)),    # Measure all qubits
    ("0 "*N + "1 "*N, ("0"*N, "1"*N)),  # Arbitrary whitespace from qiskit
    ("0"*N + "1"*2, ("0"*N, "1"*2))     # Measure only some qubits
])
def test_from_string(state_str: str, expected: tuple[str, str]):
    state = CircuitState.from_string(state_str, N)
    assert isinstance(state, CircuitState)
    assert state.erasure == expected[0]
    assert state.measure == expected[1]
