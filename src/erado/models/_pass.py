from erado.models._core import (
    EXEMPT_GATES,
    SNAPSHOT_GATES,
    CircuitState,
    ShotCallback,
    ShotInfo,
)

from qiskit import QuantumCircuit
from qiskit.circuit import (
    QuantumRegister,
    ClassicalRegister,
    IfElseOp,
    Measure,
    Reset,
)
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.dagcircuit import DAGCircuit
from qiskit.providers import BackendV2

from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    pauli_error,
)

from itertools import chain
from typing import override
from copy import deepcopy
from collections import Counter
from collections.abc import Sequence


class ErasurePass(TransformationPass):
    """Transpiler pass implementing erasable qubits.

    This bakes conditional gates into arbitrary quantum circuits representing qubit erasure logic.
    A classical register `ERASURE_CREG_NAME` is added, with one bit representing the Boolean erasure
    state for each qubit in the circuit. Any gates on erased qubits are disabled via IF statements
    on the relevant erasure bits.

    A single ancilla qubit `ERASER_QREG_NAME` is also added, which is solely used to populate erasure
    events via the noise model provided by `add_erasure_noise`.

    The main benefit of this method is a single circuit layout which can be batch-simulated.
    The main drawback of this method is that conditional logic is considerably slower than a 'pure'
    quantum circuit.

    Note that due to the in-circuit conditional logic, populating erasures after gates is more efficient
    than populating them before gates; this is the default behaviour, but either approach can be selected.

    See `example_ErasurePass` for example usage.
    """
    ERASURE_CREG_NAME = "erased"
    ERASER_QREG_NAME = "q_eraser"

    def __init__(self, erasure_before_gates: bool = False):
        """Construct a new `ErasurePass` transpiler pass object.

        Args:
            erasure_before_gates: If true, erasures are inflicted before a gate, not after.
        """
        self._erasure_before_gates = erasure_before_gates
        self._n_erasable_gates: int | None = None

        super().__init__()

    @property
    def erasure_before_gates(self) -> bool:
        """If true, erasures are inflicted before a gate, not after."""
        return self._erasure_before_gates

    @property
    def n_erasable_gates(self) -> int:
        """Contains n_erasable_gates for the most recent transpiler pass.

        Raises:
            RuntimeError: If a pass has not yet ran.
        """
        if self._n_erasable_gates is None:
            raise RuntimeError("Cannot access n_erasable_gates before running a pass.")
        return self._n_erasable_gates

    @override
    def run(self, dag: DAGCircuit) -> DAGCircuit:
        # Collect all erasable quantum operations
        gates = [node for node in dag.op_nodes()
                 if node.name not in EXEMPT_GATES]
        self._n_erasable_gates = len(gates)

        # Add new classical register of qubit erasure flags
        erasure_creg = ClassicalRegister(dag.num_qubits(), ErasurePass.ERASURE_CREG_NAME)
        dag.add_creg(erasure_creg)

        # Add a single qubit used to populate erasure events
        erasure_qreg = QuantumRegister(1, ErasurePass.ERASER_QREG_NAME)
        dag.add_qreg(erasure_qreg)

        for node in gates:
            # Create a new QuantumCircuit directly containing the original gate
            gate_circuit = QuantumCircuit(QuantumRegister(bits=node.qargs), ClassicalRegister(bits=node.cargs))
            gate_circuit.append(node.op, node.qargs, node.cargs)

            # Create a new QuantumCircuit implementing a noise-controlled erasure event
            erasure_cargs = [erasure_creg[dag.find_bit(qarg)[0]] for qarg in node.qargs]
            eraser_circuit = QuantumCircuit(erasure_qreg, ClassicalRegister(bits=erasure_cargs))
            for carg in erasure_cargs:
                eraser_circuit.append(Measure(), [erasure_qreg], [carg])  # This 0 state is flipped pre-measurement by the noise channel
                eraser_circuit.append(Reset(), [erasure_qreg])

            # Instantiate mini-DAG and attach mini-registers
            mini_dag = DAGCircuit()
            n_qargs = len(node.qargs)

            mini_qreg = QuantumRegister(n_qargs, "mini_q")
            mini_dag.add_qreg(mini_qreg)

            mini_creg = ClassicalRegister(n_qargs, "mini_c")
            mini_dag.add_creg(mini_creg)

            mini_dag.add_qreg(erasure_qreg)

            # Populate mini-DAG with gate+erasure circuits, conditional on the relevant erasure flags
            if self.erasure_before_gates:
                conditional_eraser = IfElseOp((mini_creg, 0), eraser_circuit)
                conditional_gate = IfElseOp((mini_creg, 0), gate_circuit)
                mini_dag.apply_operation_back(conditional_eraser, erasure_qreg, mini_creg)
                mini_dag.apply_operation_back(conditional_gate, mini_qreg, mini_creg)
            else:
                combined_circuit = gate_circuit.tensor(eraser_circuit)
                if combined_circuit is None:
                    raise RuntimeError("Circuits could not be combined (possibly in-place tensor).")
                conditional = IfElseOp((mini_creg, 0), combined_circuit)
                mini_dag.apply_operation_back(conditional, chain(erasure_qreg, mini_qreg), mini_creg)

            # Explicitly map mini-DAG wires to global wires
            wires = {mini_qreg[i]: node.qargs[i] for i in range(n_qargs)}
            for i in range(n_qargs):
                q_index, _ = dag.find_bit(node.qargs[i])
                wires[mini_creg[i]] = erasure_creg[q_index]
            wires[erasure_qreg[0]] = erasure_qreg[0]

            # Substitute original node with mini-DAG
            dag.substitute_node_with_dag(node, mini_dag, wires)

        return dag


def get_qubit_by_name(qc: QuantumCircuit, name: str) -> int:
    """Return the index of the sole/first qubit in a qreg of a given name.

    Args:
        qc: Qiskit circuit.
        name: Quantum register name.

    Raises:
        ValueError: If no qreg could be found with the given name.

    Returns:
        Qubit index.
    """
    for qreg in qc.qregs:
        if qreg.name == name:
            return qc.find_bit(qreg[0])[0]

    raise ValueError("Could not find a qreg with the requested name.")


def add_erasure_noise(noise_model: NoiseModel, qc: QuantumCircuit, erasure_rate: float) -> None:
    """Add an erasure noise model to an `ErasurePass` circuit.

    This model populates erasure events via Pauli noise on the `ErasurePass.ERASER_QREG_NAME` ancilla.

    One should avoid using `add_all_qubit_quantum_error` in other error modes in the model, so as
    not to introduce additional noise on this ancilla. Instead, prefer to use `add_quantum_error`
    on explicit qubits, via a loop or otherwise.

    See `example_ErasurePass` for example usage.

    Args:
        noise_model: Preexisting Qiskit Aer noise model.
        qc: Qiskit circuit (must have had `ErasurePass` applied).
        erasure_rate: Uniform erasure rate.
    """
    error = pauli_error([("X", erasure_rate), ("I", 1 - erasure_rate)])
    noise_model.add_quantum_error(error, "measure", [get_qubit_by_name(qc, ErasurePass.ERASER_QREG_NAME)])


class ErasurePassJob:
    """Utility class to run `ErasurePass`-based simulations.

    Fulfills the `ErasureModel` protocol.
    """
    def __init__(
            self,
            circuit: QuantumCircuit,
            erasure_rate: float = 0.5,
            erasure_before_gates: bool = False,
        ):
        """Construct a model with a Qiskit circuit and uniform erasure rate.

        Args:
            circuit: Qiskit quantum circuit.
            erasure_rate: Uniform erasure rate.
            erasure_before_gates: If true, erasures are inflicted before a gate, not after.
        """
        self._circuit = circuit
        self._erasure_rate = erasure_rate
        self._erasure_before_gates = erasure_before_gates

        ep = ErasurePass(erasure_before_gates=erasure_before_gates)
        pm = PassManager([ep])
        self._circuit_erasure = pm.run(circuit)

        # Ensure that snapshot gates correctly apply to all qubits despite new ERASER_QREG
        for i, gate in enumerate(self._circuit_erasure.data):
            if gate.name in SNAPSHOT_GATES:
                gate.operation.num_qubits = self._circuit_erasure.num_qubits

                # Ensure the new instruction is correct by appending it, then move it to overwrite
                # the old one.
                self._circuit_erasure.append(
                    gate.operation,
                    self._circuit_erasure.qubits,
                )
                self._circuit_erasure.data[i] = self._circuit_erasure.data[-1]
                del self._circuit_erasure.data[-1]

        self._n_erasable_gates = ep.n_erasable_gates

    @property
    def circuit(self) -> QuantumCircuit:
        """Qiskit quantum circuit being simulated."""
        return self._circuit

    @property
    def circuit_erasure(self) -> QuantumCircuit:
        """Copy of circuit with `ErasurePass` applied."""
        return self._circuit_erasure

    @property
    def erasure_rate(self) -> float:
        """Uniform erasure rate."""
        return self._erasure_rate

    @property
    def erasure_before_gates(self) -> bool:
        """If true, erasures are inflicted before a gate, not after."""
        return self._erasure_before_gates

    @property
    def n_erasable_gates(self) -> int:
        """Number of erasable gates (i.e. not in `EXEMPT_GATES`) in the circuit."""
        return self._n_erasable_gates

    def run(
            self,
            backend: BackendV2,
            shots: int,
            callbacks: Sequence[ShotCallback] = [],
            **_,
        ) -> Counter[CircuitState]:
        """Execute the simulation on a given backend for some number of shots.

        This method temporarily replaces the backend's noise model with a copy with
        `add_erasure_noise` called on it. The original noise model is replaced at this method's
        completion.

        Note that due to the reliance on noisy simulation, only `AerSimulator` is supported as a
        backend; a `TypeError` will be raised if any other backend is given.

        Args:
            backend: Circuit simulator backend.
            shots: Number of shots.
            callbacks: Collection of per-shot callback functions.

        Raises:
            TypeError: If the backend is not an `AerSimulator`.

        Returns:
            A map of each `CircuitState` to the number of times it was observed.
        """
        if type(backend) is not AerSimulator:
            raise TypeError("Only AerSimulator is supported for ErasurePassJob.")

        nm_old = getattr(backend.options, "noise_model", None)
        nm_new = NoiseModel() if nm_old is None else deepcopy(nm_old)
        add_erasure_noise(nm_new, self.circuit_erasure, self.erasure_rate)
        setattr(backend.options, "noise_model", nm_new)

        result = backend.run(
            self.circuit_erasure,
            shots=shots,
            memory=len(callbacks) > 0,
        ).result()

        if len(callbacks) > 0:
            memory: list[str] = result.get_memory(self.circuit_erasure)

            for i, state in enumerate(memory):
                for callback in callbacks:
                    callback(ShotInfo(
                        self,
                        result,
                        CircuitState.from_qiskit_string(state, self.circuit.num_qubits),
                        i,
                        0,
                        i,
                        0,
                    ))

        # Restore original state of backend's noise model
        setattr(backend.options, "noise_model", nm_old)

        counts = result.get_counts()

        return Counter({CircuitState.from_qiskit_string(key, self.circuit.num_qubits): value
                        for key, value in counts.items()})


__all__ = [
    "ErasurePass",
    "get_qubit_by_name",
    "add_erasure_noise",
    "ErasurePassJob",
]
