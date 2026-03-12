Getting Started
===============

Background
----------

In classical error correction, an *erasure* is a type of error where (unlike a bit flip) a bit is lost or otherwise malfunctions, **and the location of that error is known**. If considering a noise model containing only erasures, error detection therefore comes for free, which makes error correction much easier, too.

In quantum error correction, erasures can equivalently be thought of as errors comprising some leakage mechanism (e.g. photon loss in optical qubits, or relaxation to a ground state in dual-rail oscillator qubits) detectable by a measurement orthogonal to the computational basis.

Erasure codes/channels are generally easier to decode; however, we can also more fundamentally consider *postselection* for general erasure error mitigation. In practical terms, we simply discard shots where one or more erasures occurred. This theoretically fully mitigates against the erasure channel -- if accounting for errors on the erasure checks themselves, as well as other, unheralded Pauli channels (e.g. circuit-level depolarising noise).

``erado`` can be used to simulate circuit-level erasure noise and to run postselection experiments. For more information, please see our corresponding paper: *coming very soon!*

Erasure noise models
--------------------

Erasure circuit sampler
~~~~~~~~~~~~~~~~~~~~~~~

``erado`` provides the :class:`erado.models.ErasureModel` concept; this is a `protocol <https://typing.python.org/en/latest/spec/protocol.html>`__ which represents a :class:`qiskit.circuit.QuantumCircuit` with an erasure rate :math:`p_e`. The :meth:`~erado.models.ErasureModel.run` method can then be used to run the circuit with erasure noise on a given backend.

We simulate erasure noise by the following key rules:

#. any gate in the circuit can set its qubit arguments to an erased state with uniform probability :math:`p_e`;
#. any gate with an erased qubit argument(s) is turned into a no-op, i.e. the identity operation.

Two equivalent implementations of :class:`.ErasureModel` are provided. The first of these is the :class:`erado.models.ErasureCircuitSampler` class, which works by deleting gates from the circuit corresponding to a sampled erasure-event distribution, on a per-shot basis::

    from erado import (
        circuits,
        models,
    )

    import qiskit_aer


    # Any Qiskit circuit works, but erado.circuits provides a few for convenience
    n_qubits = 5
    circuit = circuits.qft_linear(n_qubits)
    circuit.measure_all()

    erasure_rate = 0.01
    erasure_model = models.ErasureCircuitSampler(circuit, erasure_rate)

    # The erasure model can run on any compatible backend, e.g. Qiskit Aer's standard simulator
    backend = qiskit_aer.AerSimulator(method="statevector")
    counts = erasure_model.run(backend, shots=1000)
    print(counts)

The ``counts`` object returned by :meth:`~erado.models.ErasureModel.run` is a :class:`~collections.Counter` [:class:`erado.models.CircuitState`], where each :class:`.CircuitState` contains an ``erasure`` field (a bitstring representing an erasure check per qubit) and a ``measure`` field (observed computational state bitstring as returned by the Qiskit backend).

    💡 **TIP:**

    You can load `OpenQASM <https://openqasm.com>`__ circuits (e.g. from a ``.qasm`` file) easily with the :func:`qiskit.qasm2.load`/:func:`~qiskit.qasm2.loads` functions.

Erasure transpiler pass
~~~~~~~~~~~~~~~~~~~~~~~

The second implementation is the :class:`erado.models.ErasurePassJob`. This instead uses a circuit transpiler pass to wrap every circuit gate with a classical ``if`` conditioned on the erasure state of each qubit, which is stored in an auxiliary classical bit register.

As it also implements the :class:`.ErasureModel` protocol, usage can be identical::

    from erado import (
        circuits,
        models,
    )

    import qiskit_aer


    # Any Qiskit circuit works, but erado.circuits provides a few for convenience
    n_qubits = 5
    circuit = circuits.qft_linear(n_qubits)
    circuit.measure_all()

    erasure_rate = 0.01
    erasure_model = models.ErasurePassJob(circuit, erasure_rate)

    # The erasure model can run on any compatible backend, e.g. Qiskit Aer's standard simulator
    backend = qiskit_aer.AerSimulator(method="statevector")
    counts = erasure_model.run(backend, shots=1000)
    print(counts)

Alternatively, you can explicitly transpile the circuit yourself (with the underlying :class:`.ErasurePass` class) and run the circuit directly on the backend, by adding the erasure logic via your own :class:`qiskit_aer.noise.NoiseModel`::

    from qiskit import transpiler

    n_qubits = 5
    circuit = circuits.qft_linear(n_qubits)
    circuit.measure_all()

    # Manually transpile the circuit (adding 'if' guards etc.)
    pass_manager = transpiler.PassManager([models.ErasurePass()])
    circuit_erasure = pass_manager.run(circuit)

    # Add the erasure noise logic to a brand new Qiskit Aer NoiseModel
    erasure_rate = 0.01
    noise_model = qiskit_aer.noise.NoiseModel()
    models.add_erasure_noise(noise_model, circuit_erasure, erasure_rate)

    # Run directly via the backend
    backend = qiskit_aer.AerSimulator(method="statevector", noise_model=noise_model)
    result = backend.run(circuit_erasure, shots=1000).result()

Importantly -- across all of these methods -- you can configure your backend with additional noise models and other configurations as you wish!

    ⚠️ **NOTE:**

    Due to reliance on :class:`qiskit_aer.noise.NoiseModel`, the erasure transpiler pass approach is only compatible with the :class:`qiskit_aer.AerSimulator` backend.

..

    ⛔ **WARNING:**

    The erasure transpiler pass adds both an auxiliary classical register and an auxiliary quantum register for its internal logic. Therefore, you should avoid using :meth:`~qiskit_aer.noise.NoiseModel.add_all_qubit_quantum_error`, instead defining your other noise channels explicitly with :meth:`~qiskit_aer.noise.NoiseModel.add_quantum_error`.

Simulation frontend
-------------------

Instead of using either of these erasure models directly, we also provide the :class:`erado.frontend.ErasureSimFrontend` class, which wraps the simulation to add some key optional features:

#. postselection, where shots with erasures are rejected and the simulation continues until the target number of shots are accepted;
#. check noise, where erasure detection is affected by classical false-positive and false-negative rates;
#. per-shot circuit fidelity.

Using the frontend is generally as simple as injecting the desired erasure model dependency alongside the backend and circuit::

    from erado import (
        circuits,
        models,
        fidelity,
        frontend,
    )

    import qiskit_aer


    # If requesting fidelities, the circuit must contain an end-of-line state snapshot
    n_qubits = 5
    circuit = circuits.qft_linear(n_qubits)
    circuit.save_statevector(label=fidelity.STATE_LABEL, pershot=True)
    circuit.measure_all()

    erasure_rate = 0.01
    erasure_model = models.ErasureCircuitSampler(circuit, erasure_rate)

    # You can also seed the ErasureModel RNG for replicability
    erasure_model.seed(0)

    backend = qiskit_aer.AerSimulator(method="statevector")

    sim_frontend = frontend.ErasureSimFrontend(
        model=erasure_model,
        false_positive_rate=0.005,
        false_negative_rate=0.010,  # false negatives harm accepted circuit fidelity
    )

    results = sim_frontend.run(
        backend=backend,
        shots=1000,
        postselect=True,
        get_fidelities=True,
    )

The ``results`` object returned by :meth:`~erado.frontend.ErasureSimFrontend.run` is an :class:`erado.frontend.ErasureSimResults` struct, containing not only the counts but a range of data about the simulation run, such as rejection rate and fidelities (if requested).

For each shot, the circuit fidelity is reported with respect to the cached ideal representation of the circuit.

    💡 **TIP:**

    ``get_fidelities`` also works for density-matrix simulations (i.e. ``AerSimulator(method="densitymatrix")``), in which case ``circuit.save_density_matrix`` must be used instead.

    Also, note that the use of ``label=fidelity.STATE_LABEL`` and ``pershot=True`` is non-optional.
