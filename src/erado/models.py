"""Provides the underlying erasure simulation models."""

from erado.util import MultiprocessingRNG, NPVector

from qiskit import QuantumCircuit
from qiskit.circuit import QuantumRegister, ClassicalRegister, IfElseOp, Measure, Reset, Qubit, CircuitInstruction
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.dagcircuit import DAGCircuit
from qiskit.providers import BackendV2 as Backend

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

import numpy as np

from pydantic import BaseModel, ConfigDict, ModelWrapValidatorHandler, model_validator, ValidationError

from itertools import chain
from typing import Protocol, Self, override
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed, wait
from collections import Counter
from collections.abc import Generator
import os
import logging
import multiprocessing


_logger = logging.getLogger(__name__)


class CircuitState(BaseModel):
    """Data structure representing the observed state of a quantum circuit.

    This is equivalent to a tuple of the state of erasure checks on all qubits in the circuit (the
    `erasure` field) and the computational state of measured qubits in the same format as is
    returned by Qiskit backends (the `measure` field).
    """
    erasure: str
    measure: str

    model_config = ConfigDict(frozen=True)  # 'frozen' makes this struct immutable and hashable

    @classmethod
    def from_string(cls, state: str, n_qubits: int) -> Self:
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

    @model_validator(mode="wrap")
    @classmethod
    def deserialise(cls, value: object, handler: ModelWrapValidatorHandler[Self]) -> Self:
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
                erasure, measure = value.split(",", 1)
                return cls(erasure=erasure, measure=measure)
            except ValueError:
                raise ValidationError("Could not deserialise CircuitState from string.")
        return handler(value)


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

    def run(self, backend: Backend, shots: int) -> Counter[CircuitState]:
        """Execute an erasure simulation using this model.

        Args:
            backend: Circuit simulator backend.
            shots: Number of shots.

        Returns:
            A map of each `CircuitState` to the number of times it was observed.
        """
        ...


EXEMPT_GATES = ["barrier", "measure"]
"""Circuit elements which are never involved in erasure events."""


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
            erasure_before_gates: bool = False
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

    def run(self, backend: Backend, shots: int) -> Counter[CircuitState]:
        """Execute the simulation on a given backend for some number of shots.

        This method temporarily replaces the backend's noise model with a copy with
        `add_erasure_noise` called on it. The original noise model is replaced at this method's
        completion.

        Note that due to the reliance on noisy simulation, only `AerSimulator` is supported as a
        backend; a `TypeError` will be raised if any other backend is given.

        Args:
            backend: Circuit simulator backend.
            shots: Number of shots.

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

        result = backend.run(self.circuit_erasure, shots=shots).result()

        setattr(backend.options, "noise_model", nm_old)

        counts = result.get_counts()

        return Counter({CircuitState.from_string(key, self.circuit.num_qubits): value
                        for key, value in counts.items()})


class ErasureCircuitSampler(MultiprocessingRNG):
    """Custom simulation wrapper implementing erasure noise on arbitrary circuits.

    This class dynamically samples circuits by deleting gates based on erasure events.
    A lookup table is precomputed upon construction which provides the set of gates deleted
    by each possible erasure event.

    The main benefit of this method is that strictly no overhead is introduced on circuits.
    The main drawback of this method is that circuits are individually sampled and simulated.

    Note that the `seed` method (provided via `MultiprocessingRNG`) correctly affects/overrides
    the seed behaviour of the backend provided to `run`.

    Fulfills the `ErasureModel` protocol.

    See `example_ErasureCircuitSampler` for example usage.
    """
    def __init__(
            self,
            circuit: QuantumCircuit,
            erasure_rate: float = 0.5,
            erasure_before_gates: bool = False,
            timeout: float | None = 10.0
        ):
        """Construct a model with a Qiskit circuit and uniform erasure rate.

        Args:
            circuit: Qiskit quantum circuit.
            erasure_rate: Uniform erasure rate.
            erasure_before_gates: If true, erasures are inflicted before a gate, not after.
            timeout: Maximum time allowed per shot before forcibly terminating.
        """
        self._circuit = circuit
        self._erasure_rate = erasure_rate
        self._erasure_before_gates = erasure_before_gates
        self._timeout = timeout

        self._main_pid = os.getpid()  # Used for cleaner error handling whilst multiprocessing

        self._precompute_lut()

    @property
    def circuit(self) -> QuantumCircuit:
        """Qiskit quantum circuit being simulated."""
        return self._circuit

    @property
    def erasure_rate(self) -> float:
        """Uniform erasure rate."""
        return self._erasure_rate

    @property
    def erasure_before_gates(self) -> bool:
        """If true, erasures are inflicted before a gate, not after."""
        return self._erasure_before_gates

    @property
    def timeout(self) -> float | None:
        """Maximum time allowed per shot before forcibly terminating."""
        return self._timeout

    def n_gates(self) -> int:
        """Total number of gates in the circuit."""
        return len(self.circuit.data)

    def erasable_gates(self) -> Generator[tuple[int, CircuitInstruction], None, None]:
        """Iterate through all erasable gates in the circuit.

        Yields:
            tuple[int,CircuitInstruction]: Index and instruction for each erasable gate.
        """
        return ((i, g) for i, g in enumerate(self.circuit.data)
                if g.name not in EXEMPT_GATES)

    @property
    def n_erasable_gates(self) -> int:
        """Number of erasable gates (i.e. not in `EXEMPT_GATES`) in the circuit."""
        return len(list(self.erasable_gates()))

    def _precompute_lut(self) -> None:
        """Generate map of erasable gate index to list of gates to erase."""
        self._lut: dict[int, list[int]] = {}
        for i, gate in self.erasable_gates():
            gates_to_remove = []
            for qubit in gate.qubits:
                start = i if self.erasure_before_gates else i + 1
                gates_to_remove.extend((j+start for j, g in enumerate(self.circuit.data[start:])
                                        if qubit in g.qubits and g.name not in EXEMPT_GATES))
            self._lut[i] = gates_to_remove

    def sample(
            self,
            erasure_events: NPVector[np.int64] | None = None
        ) -> tuple[QuantumCircuit, NPVector[np.int64], set[Qubit]]:
        """Sample the circuit, i.e. delete gates based on erasure events.

        If erasure events (a Boolean flag for each gate in the circuit) are not provided, they are
        sampled as a Bernoulli distribution from the specified `erasure_rate`.

        Args:
            erasure_events: Binary vector dictating if an erasure occurred on each gate.

        Raises:
            ValueError: If the length of `erasure_events` does not equal `self.n_gates()`.

        Returns:
            Tuple of the sampled circuit, erasure events and set of erased qubits.
        """
        if erasure_events is None:
            erasure_events = self._rng.binomial(1, self.erasure_rate, self.n_gates())
        elif len(erasure_events) != self.n_gates():
            raise ValueError("erasure_events must have an entry for every gate in the circuit.")

        i_erasures = (i for i, x in enumerate(erasure_events)
                      if x == 1 and self.circuit.data[i].name not in EXEMPT_GATES)

        erased_qubits: set[Qubit] = set()
        gates_to_remove: set[int] = set()
        for i in i_erasures:
            gate = self.circuit.data[i]
            if any((q not in erased_qubits for q in gate.qubits)):
                erased_qubits.update(gate.qubits)
                gates_to_remove.update(self._lut[i])
            # NOTE: To match other behaviour, change this loop so that an erasure is NOT processed
            # if any of its qargs are already erased.

        erased_circuit = self.circuit.copy()
        for i in reversed(sorted(gates_to_remove)):
            del erased_circuit.data[i]

        return erased_circuit, erasure_events, erased_qubits

    def run(
            self,
            backend: Backend,
            shots: int,
            multiprocess: bool = True
        ) -> Counter[CircuitState]:
        """Execute the simulation on a given backend for some number of shots.

        As this is CPU-bound in the `sample` method, multiprocessing is used to parallelise the
        workload for considerable speedup. This can be disabled with the `multiprocess` parameter.

        If any single shot within a child process takes longer than the `timeout` property
        (default: 10 seconds) to complete, the child will kill itself. This will manifest as either
        a `TimeoutError` or `BrokenProcessPool` exception. To disable this timeout completely, set
        `timeout` to None.

        Args:
            backend: Circuit simulator backend.
            shots: Number of shots.
            multiprocess: If true, parallelise the workload over multiple processes.

        Raises:
            RuntimeError: If the resultant number of shots does not equal the `shots` argument.

        Returns:
            A map of each `CircuitState` to the number of times it was observed.
        """
        if multiprocess:
            # Invoke _run on multiple processes on subsets of the problem
            counts: Counter[str] = Counter()
            with ProcessPoolExecutor(
                    initializer=self._reseed,
                    mp_context=multiprocessing.get_context("spawn")
                ) as executor:
                max_workers = os.process_cpu_count()  # this is the default since Python 3.13
                shots_each = shots // max_workers
                counters_futures = [executor.submit(self._run, backend, shots_each) for _ in range(max_workers - 1)]
                counters_futures.append(executor.submit(self._run, backend, shots_each + (shots % max_workers)))

                for counter in as_completed(counters_futures):
                    counts += counter.result()
        else:
            counts = self._run(backend, shots)

        if counts.total() != shots:
            raise RuntimeError("Total result count does not equal requested number of shots.")

        return Counter({CircuitState.from_string(key, self.circuit.num_qubits): value
                        for key, value in counts.items()})

    def _run(self, backend: Backend, shots: int) -> Counter[str]:
        # Execute all shots in serial (a bareboned thread pool is used just to allow for timeout)
        counts: Counter[str] = Counter()
        with ThreadPoolExecutor(max_workers=1) as executor:
            for _ in range(shots):
                circuit, _, erased_qubits = self.sample()

                future = executor.submit(lambda: backend.run(
                        circuit,
                        shots=1,
                        seed_simulator=self._rng.integers(2**32)
                    ).result())  # type: ignore # qiskit.providers.BackendV2 does not correctly annotate run method
                _, not_done = wait((future,), timeout=self.timeout)

                # If timed out, cleanly throw/kill based on the status of this process
                if len(not_done) > 0:
                    _logger.error("ErasureCircuitSampler shot timed out and will now attempt to terminate.")
                    pid = os.getpid()
                    if pid == self._main_pid:
                        raise TimeoutError("Single shot timed out.")
                    else:
                        os.kill(os.getpid(), 9)

                erasure_state = "".join(("1" if q in erased_qubits else "0"
                                        for q in reversed(circuit.qubits)))

                state: str = erasure_state + next(iter(future.result().get_counts()))
                counts[state] += 1

        return counts
