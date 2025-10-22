"""Tests for expected behaviour of `ErasureSimFrontend`."""

from erado.models import ErasureModel, ErasurePassJob, ErasureCircuitSampler
from erado.frontend import ErasureSimFrontend, ErasureSimResults
from erado.circuits import ghz_circuit
# TODO: lint rule for imports on newlines with commas?

from qiskit import ClassicalRegister
from qiskit_aer import AerSimulator


N = 4
"""Number of qubits to use in these tests, unless otherwise specified."""


def test_measure_EOL_all(model_type: type[ErasureModel]):
    """Test basic simulator usage, assuming end-of-line measurements on all qubits."""
    circuit = ghz_circuit(N)
    circuit.measure_all()

    backend = AerSimulator(method="statevector", device="CPU")
    shots = 10
    erasure_rate = 50e-6

    model = model_type(circuit=circuit, erasure_rate=erasure_rate)
    frontend = ErasureSimFrontend(model=model)
    results = frontend.run(backend, shots)

    assert isinstance(results, ErasureSimResults)
    assert results.shots == shots
    assert results.counts.total() == shots


def test_measure_EOL_some(model_type: type[ErasureModel]):
    """Test basic simulator usage, assuming end-of-line measurements on only some qubits."""
    circuit = ghz_circuit(N)

    circuit.add_register(ClassicalRegister(N-2, "meas"))
    circuit.barrier()
    for i in range(N-2):
        circuit.measure(i, i)

    backend = AerSimulator(method="statevector", device="CPU")
    shots = 10
    erasure_rate = 50e-6

    model = model_type(circuit=circuit, erasure_rate=erasure_rate)
    frontend = ErasureSimFrontend(model=model)
    results = frontend.run(backend, shots)

    assert isinstance(results, ErasureSimResults)
    assert results.shots == shots
    assert results.counts.total() == shots


def test_multiprocessing_deadlock():
    """Test for regressions in the Qiskit multiprocessing bug.

    Qiskit seems to introduce some buggy behaviour in backend runs due to its own use of
    multithreading. If a backend simulation job is performed before a multiprocess-enabled
    `ErasureCircuitSampler` run, this run can deadlock, even if a new backend object is created.

    This was originally only 'solved' by performing simulation runs in strictly different programs.
    However, it now seems that I've fixed it by some careful use of multiprocessing context
    settings. This test is designed to catch any regressions in this bugfix.
    """
    circuit = ghz_circuit(N)
    circuit.measure_all()

    backend = AerSimulator(method="statevector", device="CPU")
    shots = 10
    erasure_rate = 50e-6

    circuit_sampler = ErasureCircuitSampler(circuit=circuit, erasure_rate=erasure_rate)
    pass_job = ErasurePassJob(circuit=circuit, erasure_rate=erasure_rate)

    circuit_sampler.run(backend, shots)
    pass_job.run(backend, shots)
    circuit_sampler.run(backend, shots)
