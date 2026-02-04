"""Tests for expected behaviour of `ErasureSimFrontend`."""

from erado.models import (
    ErasureModel,
    ErasurePassJob,
    ErasureCircuitSampler,
)
from erado.frontend import (
    ErasureSimFrontend,
    ErasureSimResults,
)
import erado.circuits as circuits

from qiskit import ClassicalRegister
from qiskit_aer import AerSimulator


N = 4
"""Number of qubits to use in these tests, unless otherwise specified."""


def test_measure_EOL_all(model_type: type[ErasureModel]):
    """Test basic simulator usage, assuming end-of-line measurements on all qubits."""
    circuit = circuits.ghz(N)
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
    circuit = circuits.ghz(N)

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
    """Test for regressions in multiprocessing hanging bugs.

    Qiskit can introduce some buggy behaviour in backend runs due to its own use of
    multithreading. If a backend simulation job is performed before a multiprocess-enabled
    `ErasureCircuitSampler` run, this run can deadlock, even if a new backend object is created.

    This is avoided by careful use of multiprocessing contexts and start methods (i.e. avoiding
    `fork` on POSIX Python <3.14).
    """
    circuit = circuits.ghz(N)
    circuit.measure_all()

    backend = AerSimulator(method="statevector", device="CPU")
    shots = 10
    erasure_rate = 50e-6

    circuit_sampler = ErasureCircuitSampler(circuit=circuit, erasure_rate=erasure_rate)
    pass_job = ErasurePassJob(circuit=circuit, erasure_rate=erasure_rate)

    circuit_sampler.run(backend, shots, multiprocess=True)
    pass_job.run(backend, shots)
    circuit_sampler.run(backend, shots, multiprocess=True)
