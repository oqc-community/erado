from erado.models import (
    ErasureCircuitSampler,
    ErasurePassJob,
)
from erado.frontend import (
    ErasureSimFrontend,
    ErasureSimResults,
)
from erado.util import (
    get_series,
    working_directory,
)
import erado.circuits as circuits

from qiskit import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
)

import numpy as np
from scipy.stats import binomtest

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from dataclasses import dataclass
import time
from pathlib import Path
import csv


ROOT_DIR = Path("data")
FIGURE_DIR = Path("figures")


@dataclass
class NoiseParams():
    erasure_rate: float = 0
    false_positive_rate: float = 0
    false_negative_rate: float = 0
    gate_error_1Q: float = 0
    gate_error_2Q: float = 0


def run_simulation(
        noise_params: NoiseParams,
        n: int,
        shots: int = 5000,
        print_circuits: bool = False
    ):
    print(f"n = {n}")

    circuit = circuits.qft_linear(n)
    circuit.measure_all()
    if print_circuits:
        print("Raw circuit:")
        print(circuit)

    # Default basis gates used by Qiskit error model, defined here for clarity and consistency
    basis_gates_1Q = ["rz", "sx"]
    basis_gates_2Q = ["cx"]
    noise_model = NoiseModel()

    # Add Pauli noise to model
    # (if rates are zero, qiskit will ignore them as 'ideal', so no need to make conditional here)
    for q in range(n):
        error_1Q = depolarizing_error(noise_params.gate_error_1Q, 1)
        noise_model.add_quantum_error(error_1Q, basis_gates_1Q, [q])

        error_2Q = depolarizing_error(noise_params.gate_error_2Q, 2)
        for q_other in range(n):
            noise_model.add_quantum_error(error_2Q, basis_gates_2Q, [q, q_other])

    print(noise_model)
    backend = AerSimulator(method="statevector", device="GPU", noise_model=noise_model)

    # Transpile circuit for the above basis gates
    pass_manager = generate_preset_pass_manager(backend=backend)
    circuit_transpiled = pass_manager.run(circuit)
    if print_circuits:
        print("Transpiled circuit:")
        print(circuit_transpiled)
    print(f"depth = {circuit_transpiled.depth()}")

    model = ErasureCircuitSampler(circuit=circuit_transpiled,
                                  erasure_rate=noise_params.erasure_rate,
                                  timeout=None)
    # model = ErasurePassJob(circuit=circuit_transpiled,
    #                        erasure_rate=noise_params.erasure_rate)
    frontend = ErasureSimFrontend(model=model,
                                  noisy_checks=True,
                                  false_positive_rate=noise_params.false_positive_rate,
                                  false_negative_rate=noise_params.false_negative_rate)

    t0 = time.time()
    results = frontend.run(backend, shots, postselect=True)
    t1 = time.time()
    dt = t1 - t0

    print(f"Simulation took {dt} seconds.")

    return results, dt


def example_QFT():
    # Current dimon noise model
    noise_params = NoiseParams(erasure_rate=50e-6,
                               false_positive_rate=0.005,
                               false_negative_rate=0.005)

    run_simulation(noise_params, 16)


def example_QFT_sweep(plot_error_bars=True):
    # Current dimon noise model
    noise_params = NoiseParams(
        erasure_rate=50e-6,
        false_positive_rate=0.005,
        false_negative_rate=0.005,
        gate_error_1Q=0.001,
        gate_error_2Q=0.01,
    )

    num_qubits = np.array(range(2, 17))
    results_list = list[ErasureSimResults]()
    simulation_time = np.zeros(len(num_qubits))
    intervals = np.zeros((2, len(num_qubits)))

    log_i = 0
    filepath_log_exists = True
    filepath_log = Path()
    while filepath_log_exists:
        log_i += 1
        filepath_log = Path(f"log{log_i}.csv")
        filepath_log_exists = filepath_log.is_file()

    for i, n in enumerate(num_qubits):
        filepath = Path(f"qft_sweep_n{n}.json")
        if filepath.is_file():
            with open(filepath, "rb") as file:
                results = ErasureSimResults.model_validate_json(file.read())
        else:
            results, time = run_simulation(noise_params, n)
            with open(filepath, "w") as file:
                file.write(results.model_dump_json(indent=4) + "\n")
            simulation_time[i] = time
            with open(filepath_log, "w") as file_log:
                log_writer = csv.writer(file_log)
                log_writer.writerow(num_qubits)
                log_writer.writerow(simulation_time)

        results_list.append(results)

        test = binomtest(results.n_rejected, results.shots)
        intervals[0, i], intervals[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate = get_series(results_list, "rejection_rate")
    circuit_depth = get_series(results_list, "circuit_depth")
    n_erasable_gates = get_series(results_list, "n_erasable_gates")
    fidelity = get_series(results_list, "fidelity")

    if plot_error_bars:
        yerr = np.apply_along_axis(lambda row: np.abs(row - rejection_rate), 1, intervals)
    else:
        yerr = None

    p = noise_params.erasure_rate
    rejection_rate_theoretical = 1 - (1 - p)**n_erasable_gates

    with working_directory(FIGURE_DIR):
        fig1, ax1 = plt.subplots(1)
        ax1.errorbar(num_qubits, rejection_rate, yerr, fmt="x-")
        ax1.plot(num_qubits, rejection_rate_theoretical, "--", color="grey")
        ax1.set_xlabel("Number of qubits, n")
        ax1.set_ylabel("Rejection rate")
        fig1.savefig("figure1.pdf")
        fig1.savefig("figure1.png")

        fig2, ax2 = plt.subplots(1)
        ax2.errorbar(circuit_depth, rejection_rate, yerr, fmt="x-")
        ax2.plot(circuit_depth, rejection_rate_theoretical, "--", color="grey")
        ax2.set_xlabel("Circuit depth")
        ax2.set_ylabel("Rejection rate")
        fig2.savefig("figure2.pdf")
        fig2.savefig("figure2.png")

        fig3, ax3 = plt.subplots(1)
        ax3.plot(num_qubits, circuit_depth, "x-")
        ax3.set_xlabel("Number of qubits, n")
        ax3.set_ylabel("Circuit depth")
        fig3.savefig("figure3.pdf")
        fig3.savefig("figure3.png")

        fig4, ax4 = plt.subplots(1)
        ax4.plot(num_qubits, n_erasable_gates, "x-")
        ax4.set_xlabel("Number of qubits, n")
        ax4.set_ylabel("Number of (erasable) gates, g")
        fig4.savefig("figure4.pdf")
        fig4.savefig("figure4.png")

        fig5, ax5 = plt.subplots(1)
        ax5.errorbar(n_erasable_gates, rejection_rate, yerr, fmt="x-")
        ax5.plot(n_erasable_gates, rejection_rate_theoretical, "--", color="grey")
        ax5.set_xlabel("Number of (erasable) gates, g")
        ax5.set_ylabel("Rejection rate")
        fig5.savefig("figure5.pdf")
        fig5.savefig("figure5.png")

        fig6, ax6 = plt.subplots(1)
        ax6.plot(num_qubits, fidelity, "x-")
        ax6.set_xlabel("Number of qubits, n")
        ax6.set_ylabel("Fidelity")
        fig6.savefig("figure6.pdf")
        fig6.savefig("figure6.png")


def plot_ideal_v_noisy(plot_error_bars=True):
    num_qubits = np.array(range(2, 17))

    # Load ideal data
    results_list_ideal = list[ErasureSimResults]()
    intervals_ideal = np.zeros((2, len(num_qubits)))
    for i, n in enumerate(num_qubits):
        filepath = Path("ideal") / f"qft_sweep_n{n}.json"
        with open(filepath, "rb") as file:
            results = ErasureSimResults.model_validate_json(file.read())

        results_list_ideal.append(results)

        test = binomtest(results.n_rejected, results.shots)
        intervals_ideal[0, i], intervals_ideal[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate_ideal = get_series(results_list_ideal, "rejection_rate")
    circuit_depth = get_series(results_list_ideal, "circuit_depth")
    n_erasable_gates = get_series(results_list_ideal, "n_erasable_gates")

    # Load noisy data
    # (assumes circuit_depth and n_erasable_gates are the same)
    results_list_noisy = list[ErasureSimResults]()
    intervals_noisy = np.zeros((2, len(num_qubits)))
    for i, n in enumerate(num_qubits):
        filepath = Path("noisy") / f"qft_sweep_n{n}.json"
        with open(filepath, "rb") as file:
            results = ErasureSimResults.model_validate_json(file.read())

        results_list_noisy.append(results)

        test = binomtest(results.n_rejected, results.shots)
        intervals_noisy[0, i], intervals_noisy[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate_noisy = get_series(results_list_noisy, "rejection_rate")

    if plot_error_bars:
        yerr_ideal = np.apply_along_axis(lambda row: np.abs(row - rejection_rate_ideal), 1, intervals_ideal)
        yerr_noisy = np.apply_along_axis(lambda row: np.abs(row - rejection_rate_noisy), 1, intervals_noisy)
    else:
        yerr_ideal = None
        yerr_noisy = None

    p = 50e-6
    rejection_rate_theoretical = 1 - (1 - p)**n_erasable_gates

    def plot(ax: Axes, xdata, xlabel):
        noisy = ax.errorbar(xdata, rejection_rate_noisy, yerr_noisy, fmt="x-", label="noisy checks (falsepos = falseneg = 0.005)")
        ideal = ax.errorbar(xdata, rejection_rate_ideal, yerr_ideal, fmt="x-", label="ideal checks")
        theoretical = ax.plot(xdata, rejection_rate_theoretical, "--", color="gray", label="ideal checks (theoretical)")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Rejection rate")
        ax.set_title(f"QFT (linear connectivity) postselection, erasure rate {p}")

        # Customise order of items in legend
        ax.legend(handles=[noisy, ideal, theoretical[0]])

    with working_directory(FIGURE_DIR):
        fig1, ax1 = plt.subplots()
        plot(ax1, num_qubits, "Number of qubits, n")
        fig1.savefig("figure1.pdf")
        fig1.savefig("figure1.png")

        fig2, ax2 = plt.subplots()
        plot(ax2, circuit_depth, "Circuit depth")
        fig2.savefig("figure2.pdf")
        fig2.savefig("figure2.png")

        fig3, ax3 = plt.subplots()
        plot(ax3, n_erasable_gates, "Number of (erasable) gates, g")
        fig3.savefig("figure3.pdf")
        fig3.savefig("figure3.png")


def plot_times():
    def plot(ax: Axes):
        for filepath in sorted(Path(".").glob("*.csv")):
            with open(filepath, "r") as file:
                file_reader = csv.reader(file)
                num_qubits = np.array(next(file_reader), dtype=int)
                time = np.array(next(file_reader), dtype=float)

            point_style = "x" if "cpu" in filepath.stem else "."
            line_style = "-" if "sampler" in filepath.stem else "--"
            fmt = point_style + line_style
            label = filepath.stem.replace("log-", "")

            ax.plot(num_qubits, time, fmt, label=f"{label} ({sum(time)})")

        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("Simulation time (seconds)")
        ax.legend()
        ax.set_title("ErasureCircuitSampler/ErasurePass (with total time in seconds)")

    with working_directory(FIGURE_DIR):
        fig1, ax1 = plt.subplots()
        plot(ax1)
        fig1.savefig("figure-time.pdf")
        fig1.savefig("figure-time.png")

        fig2, ax2 = plt.subplots()
        ax2.set_yscale("log")
        plot(ax2)
        fig2.savefig("figure-time-log.pdf")
        fig2.savefig("figure-time-log.png")


if __name__ == "__main__":
    matplotlib.rcParams["savefig.dpi"] = 300
    matplotlib.rcParams["savefig.bbox"] = "tight"

    with working_directory(ROOT_DIR):
        # example_QFT()
        example_QFT_sweep(plot_error_bars=True)
        # plot_ideal_v_noisy(plot_error_bars=True)
        # plot_times()
