def example_ErasurePass():
    import erado.circuits as circuits
    from erado.models import (
        ErasurePass,
        add_erasure_noise,
    )

    from qiskit.transpiler import PassManager
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel


    n = 8
    qc = circuits.ghz(n)
    qc.measure_all()

    print(qc)

    # You can either set up the ErasurePass model manually:
    pm = PassManager([ErasurePass(erasure_before_gates=False)])
    qc_erasure = pm.run(qc)

    print(qc_erasure)

    erasure_rate = 0.5
    noise_model = NoiseModel()
    add_erasure_noise(noise_model, qc_erasure, erasure_rate)

    import time
    backend = AerSimulator(method="statevector", device="GPU", noise_model=noise_model)
    shots = 5000
    t0 = time.time()
    result = backend.run(qc_erasure, shots=shots).result()
    t1 = time.time()
    print(result.get_counts())

    # ...or preferably, just use the ErasurePassJob class which wraps this whole process as an ErasureModel:
    # erasure_simulator = ErasurePassJob(qc, erasure_rate)
    # counts = erasure_simulator.run(backend, shots)
    # print(counts)

    dt = t1 - t0
    print(f"Time: {dt} seconds")


def example_ErasureCircuitSampler():
    import erado.circuits as circuits
    from erado.models import ErasureCircuitSampler

    from qiskit_aer import AerSimulator

    import time


    seed = 0  # None or omit for fresh entropy

    backend = AerSimulator(method="statevector", device="GPU")

    n = 8
    qc = circuits.ghz(n)
    qc.measure_all()
    print(qc)

    # shots = 1000000
    # t0 = time.time()
    # result = backend.run(qc, shots=shots).result()
    # t1 = time.time()
    # print(result.get_counts())

    erasure_rate = 0.5
    ErasureCircuitSampler.seed(seed)
    erasure_simulator = ErasureCircuitSampler(qc, erasure_rate=erasure_rate, erasure_before_gates=False)
    shots = 5000
    t0 = time.time()
    counts = erasure_simulator.run(backend, shots)
    t1 = time.time()
    print(counts)

    dt = t1 - t0
    print(f"Time: {dt} seconds")


def example_ErasureSimFrontend():
    import erado.circuits as circuits
    from erado.models import (
        ErasureCircuitSampler,
        ErasurePassJob,
    )
    from erado.frontend import ErasureSimFrontend

    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import (
        NoiseModel,
        depolarizing_error,
    )

    import time


    # Noise model
    erasure_rate = 50e-6
    false_positive_rate = 0.005 #how many negatives become false-pos
    false_negative_rate = 0.005 #how many positives become false-neg

    seed = 0  # None or omit for fresh entropy

    # Circuit
    n = 8
    circuit = circuits.ghz(n)
    circuit.measure_all()

    # Non-erasure noise model, e.g. depolarising
    # Note the avoidance of add_all_qubit_quantum_error so as not to interfere with ErasurePass' ancilla
    noise_model = NoiseModel()
    for q in range(n):
        noise_model.add_quantum_error(depolarizing_error(1.0, 1), ['x', 'h'], [q])

    backend = AerSimulator(method="statevector", device="GPU", noise_model=noise_model)
    shots = 5000

    # Erasure distribution
    model = ErasureCircuitSampler(circuit=circuit,
                                  erasure_rate=erasure_rate)
    ErasureCircuitSampler.seed(seed)
    # model = ErasurePassJob(circuit=circuit,
    #                        erasure_rate=erasure_rate)
    frontend = ErasureSimFrontend(model=model,
                                  false_positive_rate=false_positive_rate,
                                  false_negative_rate=false_negative_rate)
    ErasureSimFrontend.seed(seed)

    t0 = time.time()
    results = frontend.run(backend, shots, postselect=True)
    t1 = time.time()

    print(results.counts)
    print(f"Target shots: {shots}")
    print(f"Number of shots rejected: {results.n_rejected}")
    print(f"Rejection rate: {results.n_rejected}/{results.shots} = {results.rejection_rate}")

    dt = t1 - t0
    print(f"Time: {dt} seconds")

    # Ideal distribution, for comparison
    counts_ideal = backend.run(circuit, shots=shots).result().get_counts()
    print(counts_ideal)


if __name__ == "__main__":
    # example_ErasurePass()
    # example_ErasureCircuitSampler()
    # example_ErasureSimFrontend()

    pass
