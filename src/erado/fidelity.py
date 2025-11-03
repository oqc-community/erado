"""Provides fidelity calculation as a per-shot callback."""
# TODO: Don't forget to update all signatures/docstrings etc.

from erado.models import (
    CircuitState,
    ShotInfo,
    SNAPSHOT_GATES,
)

from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Statevector,
    DensityMatrix,
    state_fidelity,
)

import numpy as np

from collections.abc import Generator
from multiprocessing.managers import SharedMemoryManager
import logging


_logger = logging.getLogger(__name__)


def calculate_statevector(circuit: QuantumCircuit) -> Statevector:
    """Get the statevector representing the final state of a quantum circuit.

    Any final measurements and snapshot gates are removed for the purposes of calculating the final
    statevector (this does _not_ modify the provided circuit in-place).

    Args:
        circuit: Quantum circuit.

    Raises:
        RuntimeError: If qiskit does not successfully remove final measurements.

    Returns:
        Statevector of circuit.
    """
    # Remove any final measurements (we want the final state of the circuit before observation)
    circuit_pure = circuit.remove_final_measurements(inplace=False)
    if circuit_pure is None:
        raise RuntimeError("Qiskit's remove_final_measurements did not return a circuit as requested.")

    # Also remove any snapshot calls (else constructing the `Statevector` will fail)
    for i in reversed(range(len(circuit_pure.data))):
        if circuit_pure.data[i].operation.name in SNAPSHOT_GATES:
            del circuit_pure.data[i]

    return Statevector(circuit_pure)


STATE_LABEL = "final_state"
"""Default key for snapshot gate data expected by `FidelityFunctor`."""


class FidelityFunctor:
    """Function object implementing `ShotCallback` to gather per-shot fidelity data.

    If provided as a `ShotCallback`, this function object calculates and stores the fidelity
    (along with the associated state) of each shot. These can then be accessed (and mutated) by the
    `results` generator method.
    """
    def __init__(
            self,
            shots: int,
            circuit: QuantumCircuit | None = None,
            smm: SharedMemoryManager | None = None,
        ):
        """Construct a new `FidelityFunctor`.

        The number of shots must be provided in order to preallocate the correct amount of memory
        to store the results.

        If a `SharedMemoryManager` dependency is injected, the results are stored in shared memory
        such that this functor is compatible with multiprocessing-enabled simulations.

        If possible, the quantum circuit should be provided, so that
        1) the circuit's ideal statevector is calculated once and cached, and
        2) it is guaranteed that no more or less shared memory than necessary is allocated for
            `CircuitState` representation.

        If a circuit is not provided, the fallback default allocation supports up to 64 qubits.

        Args:
            shots: Number of shots to be executed.
            circuit: Circuit to be used in simulation.
            smm: `SharedMemoryManager` instance to enable multiprocessing support.
        """
        n_qubits = circuit.num_qubits if circuit is not None else 64

        if smm is not None:
            self._fidelities = smm.ShareableList([float() for _ in range(shots)])
            self._states = smm.ShareableList([" " * n_qubits * 2 for _ in range(shots)])
        else:
            self._fidelities = [float() for _ in range(shots)]
            self._states = [str() for _ in range(shots)]

        self._circuit_sv = calculate_statevector(circuit) if circuit is not None else None

    def __call__(self, info: ShotInfo) -> None:
        """Implement `ShotCallback`.

        Args:
            info: Shot information.
        """
        index = info.start + info.i
        try:
            final_state: Statevector | DensityMatrix = info.result.data(0)[STATE_LABEL][info.i_result]
            fid = state_fidelity(
                final_state,
                self._circuit_sv if self._circuit_sv is not None else calculate_statevector(info.model.circuit)
            )
            self._fidelities[index] = fid
            self._states[index] = str(info.state)
        except KeyError:
            _logger.error(f"No {STATE_LABEL} found in this shot (state: {info.state}); using NaN for fidelity.")
            self._fidelities[index] = np.nan
            self._states[index] = str(info.state)

    def results(self) -> Generator[tuple[float, CircuitState], CircuitState, None]:
        """Iterate through all stored results.

        Optionally supports `CircuitState` as a `SendType` in order to mutate the previously-yielded
        state, e.g. to inflict erasure check noise.

        Yields:
            Tuple of fidelity and `CircuitState` corresponding to each shot.
        """
        for i in range(len(self._fidelities)):
            new_state = yield self._fidelities[i], CircuitState.from_string(self._states[i])
            if new_state is not None:
                self._states[i] = str(new_state)
        # TODO: try dummy yield with type ignore?
        # TODO: try model_construct for trusted data?
