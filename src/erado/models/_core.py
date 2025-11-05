from qiskit import QuantumCircuit
from qiskit.providers import BackendV2 as Backend
import qiskit.result

import pydantic

from typing import (
    Protocol,
    Self,
    override,
)
from collections import Counter
from collections.abc import (
    Callable,
    Sequence,
)
from dataclasses import dataclass


class CircuitState(pydantic.BaseModel):
    """Data structure representing the observed state of a quantum circuit.

    This is equivalent to a tuple of the state of erasure checks on all qubits in the circuit (the
    `erasure` field) and the computational state of measured qubits in the same format as is
    returned by Qiskit backends (the `measure` field).
    """
    erasure: str
    measure: str

    model_config = pydantic.ConfigDict(frozen=True)  # 'frozen' makes this struct immutable and hashable

    @classmethod
    def from_qiskit_string(cls, state: str, n_qubits: int) -> Self:
        """Construct a `CircuitState` from a binary string representation.

        The string is expected to be in the format yielded by a Qiskit simulation backend. For a
        circuit with n qubits, the string is expected to start with n qubit erasure states,
        followed by an arbitrary number of classical measurement bits.

        Args:
            state: Binary string representing state.
            n_qubits: Number of qubits (i.e. number of erasure checks).

        Returns:
            New `CircuitState` instance.
        """
        state = state.replace(" ", "")
        erasure = state[:n_qubits]
        measure = state[n_qubits:]
        return cls(erasure=erasure, measure=measure)

    @classmethod
    def from_string(cls, state: str) -> Self:
        """Construct a `CircuitState` from a binary string representation.

        The string is expected to be in the format yielded by `__str__`.

        Args:
            state: Binary string representing state.

        Returns:
            New `CircuitState` instance.
        """
        erasure, measure = state.split(",", 1)
        return cls(erasure=erasure, measure=measure)

    @override
    def __str__(self) -> str:
        """Serialise this `CircuitState` into a suitable string format.

        This is designed to be more readable and compact for JSON files containing a large
        dictionary of these states (as opposed to Pydantic's default found in `__repr__`).

        Examples:
            >>> print(CircuitState(erasure="000", measure="11"))
            000,11
            >>> print(repr(CircuitState(erasure="000", measure="11")))
            CircuitState(erasure='000', measure='11')

        Returns:
            String representation.
        """
        return f"{self.erasure},{self.measure}"

    @pydantic.model_validator(mode="wrap")
    @classmethod
    def deserialise(cls, value: object, handler: pydantic.ModelWrapValidatorHandler[Self]) -> Self:
        """Deserialise a `CircuitState` from a JSON-suitable string.

        Args:
            value: Serialised data.
            handler: Default Pydantic validator.

        Raises:
            ValidationError: If the input could not be deserialised.

        Returns:
            New `CircuitState` instance.
        """
        if isinstance(value, str):
            try:
                return cls.from_string(value)
            except ValueError:
                raise ValueError("Could not deserialise CircuitState from string.")
        return handler(value)


def postselect_counts(counts: Counter[CircuitState]) -> Counter[str]:
    """Filter a state counter to only non-erased states.

    Args:
        counts: `CircuitState` counter.

    Returns:
        Counter of non-erased measurement states.
    """
    counter = Counter[str]()
    for state, count in counts.items():
        if "1" not in state.erasure:
            counter[state.measure] = count
    return counter


type ShotCallback = Callable[[ShotInfo], None]
"""Per-shot callback function type."""


class ErasureModel(Protocol):
    """Protocol representing an erasure circuit simulation model.

    Any class fulfilling this protocol may be used with `frontend.ErasureSimFrontend`.
    """
    @property
    def circuit(self) -> QuantumCircuit:
        """Qiskit quantum circuit being simulated."""
        ...

    @property
    def n_erasable_gates(self) -> int:
        """Number of erasable gates (i.e. not in `EXEMPT_GATES`) in the circuit."""
        ...

    def __init__(self, circuit: QuantumCircuit, erasure_rate: float):
        """Construct a model with a Qiskit circuit and uniform erasure rate."""
        ...

    def run(
            self,
            backend: Backend,
            shots: int,
            callbacks: Sequence[ShotCallback] = [],
            **_
        ) -> Counter[CircuitState]:
        """Execute an erasure simulation using this model.

        Args:
            backend: Circuit simulator backend.
            shots: Number of shots.
            callbacks: Collection of per-shot callback functions.

        Returns:
            A map of each `CircuitState` to the number of times it was observed.
        """
        # NOTE: This signature enforces **_ to make sure all models can ignore unused kwargs.
        ...


@dataclass(frozen=True)
class ShotInfo:
    """Data structure of per-shot information provided to callbacks."""
    model: ErasureModel
    result: qiskit.result.Result
    state: CircuitState
    i: int         # Shot number within this process
    start: int     # Initial global index of this process
    i_result: int  # Shot number within the qiskit Result


SNAPSHOT_GATES = [
    "save_statevector",
    "save_density_matrix",
]
"""Circuit instructions recognised as supported state snapshots."""


EXEMPT_GATES = (
    [
        "barrier",
        "measure",
    ]
    + SNAPSHOT_GATES
)
"""Circuit instructions which are never involved in erasure events."""


__all__ = [
    "CircuitState",
    "postselect_counts",
    "ShotCallback",
    "ErasureModel",
    "ShotInfo",
    "SNAPSHOT_GATES",
    "EXEMPT_GATES",
]
