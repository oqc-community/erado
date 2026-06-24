"""Provides a selection of quantum circuits and related utilities for benchmarking."""

from collections.abc import Callable, Iterable

import qiskit.circuit
import qiskit.synthesis
import qiskit.transpiler
from qiskit_ibm_runtime.transpiler.passes import scheduling


def ghz(n: int) -> qiskit.circuit.QuantumCircuit:
    """Greenberger-Horne-Zeilinger (GHZ) state preparation.

    Args:
        n: Number of qubits.

    Returns:
        Qiskit quantum circuit.
    """
    qc = qiskit.circuit.QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)

    return qc


def qft_full(n: int) -> qiskit.circuit.QuantumCircuit:
    """Quantum Fourier transform (QFT) on all-to-all connectivity.

    This directly invokes :func:`qiskit.synthesis.synth_qft_full`.

    Args:
        n: Number of qubits.

    Returns:
        Qiskit quantum circuit.
    """
    return qiskit.synthesis.synth_qft_full(n)


def qft_linear(n: int) -> qiskit.circuit.QuantumCircuit:
    """Quantum Fourier transform (QFT) on linear connectivity.

    This directly invokes :func:`qiskit.synthesis.synth_qft_line`, which uses a construction based on
    Fowler et al. 2014 (https://arxiv.org/abs/quant-ph/0402196).

    Args:
        n: Number of qubits.

    Returns:
        Qiskit quantum circuit.
    """
    return qiskit.synthesis.synth_qft_line(n)


def pad_idling(
        circuit: qiskit.circuit.QuantumCircuit,
        max_idle_length: int = 14,
        idle_gate: Callable[[], qiskit.circuit.Gate] = qiskit.circuit.library.IGate,
        circuit_gate_time: float = 1.0,
        idle_gate_time: float = 0.8,
        sequence_min_length_ratio: float = 1.0,
    ) -> qiskit.circuit.QuantumCircuit:
    r"""Pad idle periods in a circuit with customised sequences of gates.

    This function uses a carefully-configured dynamical decoupling (DD) scheduler
    (:class:`qiskit_ibm_runtime.transpiler.passes.PadDynamicalDecoupling`) to insert copies of the given ``idle_gate``
    on all qubits during idle periods. By subjecting these idle gates to arbitrary noise models, this provides a
    straightforward way of simulating circuit-level idling error.

    The default behaviour ensures that the number of gates inserted into an idle period of length :math:`t` units of
    time is equal to

    .. math ::
        \min\left\{ t\left\lfloor\frac{t}{2}\right\rfloor , k \right\} \ ,

    where :math:`k` is ``max_idle_length``. In other words, its behaviour for increasing idle lengths :math:`t` is:

    - 1: inserts 0 gates
    - 2: inserts 2 gates
    - 3: inserts 2 gates
    - 4: inserts 4 gates
    - ...
    - 8: inserts 8 gates
    - ...ad infinitum.

    For more information, see Appendix A 'Modelling idling error' in Griffiths et al. 2026 ().

    TODO: Insert arxiv link!

    Args:
        circuit: Circuit to transform.
        max_idle_length: Maximum chain of repeated idle gates to insert in a single idle period.
        idle_gate: Gate to insert during idle periods.
        circuit_gate_time: Duration of preexisting circuit gates (arbitrary time units).
        idle_gate_time: Duration of idle gates (arbitrary time units).
        sequence_min_length_ratio: Slack parameter passed to
            :class:`qiskit_ibm_runtime.transpiler.passes.PadDynamicalDecoupling`.

    Returns:
        Circuit with padded idle periods.
    """
    durations_raw: list[tuple[str, Iterable[int] | None, float]] = [
        (gate.name, None, circuit_gate_time)
        for gate in circuit
        if gate.name != "barrier"
    ]

    durations = qiskit.transpiler.InstructionDurations(durations_raw + [("id", None, idle_gate_time)])

    idle_sequence = [
        [idle_gate()] * n
        for n in reversed(range(2, max_idle_length + 1, 2))
    ]

    # FIXME: `durations` param is deprecated as of qiskit_ibm_runtime v0.43.0 and will be removed in future.
    pass_manager = qiskit.transpiler.PassManager([
        scheduling.ALAPScheduleAnalysis(durations),
        scheduling.PadDynamicalDecoupling(  # type: ignore # Type hints do not correctly support PadDynamicalDecoupling
            durations,
            idle_sequence,
            skip_reset_qubits=False,
            sequence_min_length_ratios=[sequence_min_length_ratio]*len(idle_sequence),  # type: ignore # Parameter incorrectly hinted as int(s)
        ),
    ])

    circuit_idling = pass_manager.run(circuit)

    # Remove 'Delay' gates, leaving only the DD operations
    gates_to_remove = [i for i in range(len(circuit_idling.data))
                       if circuit_idling.data[i].name == "delay"]
    for i in reversed(gates_to_remove):
        del circuit_idling.data[i]

    return circuit_idling
