"""Defines the circuit-sampler simulation model."""

from erado import util
from erado.models import core

import qiskit
import qiskit.circuit
import qiskit.providers

import numpy as np

from concurrent import futures
import os
import logging
import collections
from collections.abc import (
    Generator,
    Sequence,
)


_logger = logging.getLogger(__name__)


class ErasureCircuitSampler(util.MultiprocessingRNG):
    """Custom simulation wrapper implementing erasure noise on arbitrary circuits.

    This class dynamically samples circuits by deleting gates based on erasure events.
    A lookup table is precomputed upon construction which provides the set of gates deleted
    by each possible erasure event.

    The main benefit of this method is that strictly no overhead is introduced on circuits.
    The main drawback of this method is that circuits are individually sampled and simulated.

    Note that the :meth:`seed` method (provided via :class:`~erado.util.MultiprocessingRNG`) correctly affects/overrides
    the seed behaviour of the backend provided to :meth:`run`.

    Fulfills the :class:`ErasureModel` protocol.

    See ``example_ErasureCircuitSampler`` for example usage.
    """
    def __init__(
            self,
            circuit: qiskit.QuantumCircuit,
            erasure_rate: float = 0.5,
            erasure_before_gates: bool = False,
            timeout: float | None = 10.0,
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
    def circuit(self) -> qiskit.QuantumCircuit:
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

    def erasable_gates(self) -> Generator[tuple[int, qiskit.circuit.CircuitInstruction]]:
        """Iterate through all erasable gates in the circuit.

        Yields:
            Tuple of index and instruction for each erasable gate.
        """
        return ((i, g) for i, g in enumerate(self.circuit.data)
                if g.name not in core.EXEMPT_GATES)

    @property
    def n_erasable_gates(self) -> int:
        """Number of erasable gates (i.e. not in :attr:`EXEMPT_GATES`) in the circuit."""
        return len(list(self.erasable_gates()))

    def _precompute_lut(self) -> None:
        """Generate map of erasable gate index to list of gates to erase."""
        self._lut = dict[int, list[int]]()
        for i, gate in self.erasable_gates():
            gates_to_remove = []
            for qubit in gate.qubits:
                start = i if self.erasure_before_gates else i + 1
                gates_to_remove.extend((j + start for j, g in enumerate(self.circuit.data[start:])
                                        if qubit in g.qubits and g.name not in core.EXEMPT_GATES))
            self._lut[i] = gates_to_remove

    def sample(
            self,
            erasure_events: util.NPVector[np.int64] | None = None,
        ) -> tuple[qiskit.QuantumCircuit, util.NPVector[np.int64], set[qiskit.circuit.Qubit]]:
        """Sample the circuit, i.e. delete gates based on erasure events.

        If erasure events (a Boolean flag for each gate in the circuit) are not provided, they are
        sampled as a Bernoulli distribution from the specified :attr:`erasure_rate`.

        Args:
            erasure_events: Binary vector dictating if an erasure occurred on each gate.

        Raises:
            ValueError: If the length of ``erasure_events`` does not equal :func:`n_gates`.

        Returns:
            Tuple of the sampled circuit, erasure events and set of erased qubits.
        """
        if erasure_events is None:
            erasure_events = self._rng.binomial(1, self.erasure_rate, self.n_gates())
        elif len(erasure_events) != self.n_gates():
            raise ValueError("erasure_events must have an entry for every gate in the circuit.")

        i_erasures = (i for i, x in enumerate(erasure_events)
                      if x == 1 and self.circuit.data[i].name not in core.EXEMPT_GATES)

        erased_qubits = set[qiskit.circuit.Qubit]()
        gates_to_remove = set[int]()
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
            backend: qiskit.providers.BackendV2,
            shots: int,
            callbacks: Sequence[core.ShotCallback] = [],
            multiprocess: bool = False,
            **_,
        ) -> collections.Counter[core.CircuitState]:
        """Execute the simulation on a given backend for some number of shots.

        As this simulation involves a single shot for each in a sequence of distinct circuits,
        multiprocessing may be used to potentially achieve notable speedup. This can be enabled
        with the ``multiprocess`` parameter. However, it may often still be faster to allow Qiskit
        to batch-process the sequence of circuits itself, so it is disabled by default.

        When using multiprocessing, if any single shot within a child process takes longer than the
        :attr:`timeout` property (default: 10 seconds) to complete, the child will kill itself. This will
        manifest as either a :class:`TimeoutError` or :class:`BrokenProcessPool` exception. To disable this
        timeout completely, set :attr:`timeout` to None.

        Args:
            backend: Circuit simulator backend.
            shots: Number of shots.
            callbacks: Collection of per-shot callback functions.
            multiprocess: If true, parallelise the workload over multiple processes.

        Raises:
            RuntimeError: If the resultant number of shots does not equal the ``shots`` argument.

        Returns:
            A map of each :class:`CircuitState` to the number of times it was observed.
        """
        if multiprocess:
            # Invoke _run_mp on multiple processes on subsets of the problem
            counts = collections.Counter[str]()
            with futures.ProcessPoolExecutor(
                    initializer=self._reseed,
                    mp_context=util.get_mp_context(),
                ) as executor:
                max_workers = os.process_cpu_count()  # this is the default since Python 3.13
                shots_each = shots // max_workers
                counters_futures = [
                    executor.submit(self._run_mp, backend, shots_each, callbacks, i * shots_each)
                    for i in range(max_workers - 1)
                ]
                counters_futures.append(
                    executor.submit(self._run_mp, backend, shots_each + (shots % max_workers), callbacks,
                                    (max_workers - 1) * shots_each),
                )

                for counter in futures.as_completed(counters_futures):
                    counts += counter.result()

            counts = collections.Counter({core.CircuitState.from_qiskit_string(key, self.circuit.num_qubits): value
                                          for key, value in counts.items()})
        else:
            counts = self._run(backend, shots, callbacks)

        if counts.total() != shots:
            raise RuntimeError("Total result count does not equal requested number of shots.")

        return counts

    def _run(
            self,
            backend: qiskit.providers.BackendV2,
            shots: int,
            callbacks: Sequence[core.ShotCallback],
        ) -> collections.Counter[core.CircuitState]:
        samples = [self.sample() for _ in range(shots)]
        circuit_list = [sample[0] for sample in samples]
        erased_qubits_list = [sample[2] for sample in samples]

        job: qiskit.providers.JobV1 = backend.run(
            circuit_list,
            shots=1,
            seed_simulator=self._rng.integers(2**32),
        )  # type: ignore # qiskit.providers.BackendV2 does not correctly annotate run method

        result = job.result()

        # Ensure counts is a list (if shots==1, qiskit will instead return the sole element)
        counts = result.get_counts()
        if not isinstance(counts, list):
            counts = [counts]

        qubit_states = [next(iter(shot)) for shot in counts]

        erasure_states = ["".join(("1" if q in erased_qubits else "0"
                                   for q in reversed(circuit.qubits)))
                          for erased_qubits, circuit in zip(erased_qubits_list, circuit_list)]

        circuit_states = [core.CircuitState.from_qiskit_string(erasure_state + qubit_state, circuit.num_qubits)
                          for erasure_state, qubit_state, circuit in zip(erasure_states, qubit_states, circuit_list)]

        if len(callbacks) > 0:
            for i, state in enumerate(circuit_states):
                for callback in callbacks:
                    callback(core.ShotInfo(
                        self,
                        result,
                        state,
                        i,
                        0,
                        0,
                        i,
                    ))

        return collections.Counter(circuit_states)

    def _run_mp(
            self,
            backend: qiskit.providers.BackendV2,
            shots: int,
            callbacks: Sequence[core.ShotCallback],
            start: int = 0,
        ) -> collections.Counter[str]:
        # Execute all shots in serial (a bareboned thread pool is used just to allow for timeout)
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            def all_shots() -> Generator[str]:
                for i in range(shots):
                    circuit, _, erased_qubits = self.sample()

                    future = executor.submit(lambda: backend.run(
                            circuit,
                            shots=1,
                            seed_simulator=self._rng.integers(2**32),
                        ).result())  # type: ignore # qiskit.providers.BackendV2 does not correctly annotate run method
                    _, not_done = futures.wait((future,), timeout=self.timeout)

                    # If timed out, cleanly throw/kill based on the status of this process
                    if len(not_done) > 0:
                        _logger.error("ErasureCircuitSampler shot timed out and will now attempt to terminate.")
                        pid = os.getpid()
                        if pid == self._main_pid:
                            raise TimeoutError("Single shot timed out.")
                        else:
                            os.kill(os.getpid(), 9)

                    result = future.result()

                    erasure_state = "".join(("1" if q in erased_qubits else "0"
                                             for q in reversed(circuit.qubits)))
                    state: str = erasure_state + next(iter(result.get_counts()))

                    for callback in callbacks:
                        callback(core.ShotInfo(
                            self,
                            result,
                            core.CircuitState.from_qiskit_string(state, self.circuit.num_qubits),
                            i,
                            start,
                            0,
                            0,
                        ))

                    yield state

            counts = collections.Counter(all_shots())

        return counts


__all__ = [
    "ErasureCircuitSampler",
]
