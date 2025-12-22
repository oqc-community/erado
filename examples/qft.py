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
import erado.fidelity as fidelity

from qiskit import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
)

import numpy as np
import scipy.stats

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from dataclasses import dataclass
import time
from pathlib import Path
import csv


ROOT_DIR = Path("data")
FIGURE_DIR = Path("figures")

DELETE_DATA = False


@dataclass
class NoiseParams():
    erasure_rate: float = 0.0
    false_positive_rate: float = 0.0
    false_negative_rate: float = 0.0
    gate_error_1Q: float = 0.0
    gate_error_2Q: float = 0.0


def run_simulation(
        noise_params: NoiseParams,
        n: int,
        shots: int = 5000,
        print_circuits: bool = False
    ):
    print(f"n = {n}")

    circuit = circuits.qft_linear(n)
    # circuit = circuits.ghz(n)
    circuit.save_statevector(label=fidelity.STATE_LABEL, pershot=True)  # type: ignore # Dynamically patched by qiksit-aer
    # circuit.save_density_matrix(label=fidelity.STATE_LABEL, pershot=True)  # type: ignore # Dynamically patched by qiksit-aer
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
    # backend = AerSimulator(method="density_matrix", device="GPU", noise_model=noise_model)

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
    model.seed(0)
    frontend = ErasureSimFrontend(model=model,
                                  noisy_checks=True,
                                  false_positive_rate=noise_params.false_positive_rate,
                                  false_negative_rate=noise_params.false_negative_rate)

    t0 = time.time()
    results = frontend.run(
        backend,
        shots,
        postselect=True,
        get_fidelities=True,
        # multiprocess=False,
    )
    t1 = time.time()
    dt = t1 - t0

    print(f"Simulation took {dt} seconds.")

    return results, dt


def example_QFT():
    # Current dimon noise model
    noise_params = NoiseParams(erasure_rate=0.01,
                               false_positive_rate=0.005,
                               false_negative_rate=0.005)

    run_simulation(noise_params, 16)


# TODO: Flesh this out to enable running all plotting functions sequentially (with cached results etc.)
n_figures: int = 0

def save_figure(fig, name: str) -> None:
    global n_figures
    n_figures += 1

    file_stem = f"figure{n_figures}-{name}"
    fig.savefig(file_stem + ".pdf")
    fig.savefig(file_stem + ".png")


def example_QFT_sweep(
        plot_error_bars=True,
        draw_grid=True,
    ):
    # Current dimon noise model
    noise_params = NoiseParams(
        erasure_rate=0.01,
        false_positive_rate=0.005,
        false_negative_rate=0.005,
        gate_error_1Q=0.001,
        gate_error_2Q=0.01,
    )

    n_qubits = np.array(range(2, 17))
    results_list = list[ErasureSimResults]()
    simulation_time = np.zeros(len(n_qubits))
    intervals = np.zeros((2, len(n_qubits)))

    log_i = 0
    filepath_log_exists = True
    filepath_log = Path()
    while filepath_log_exists:
        log_i += 1
        filepath_log = Path(f"log{log_i}.csv")
        filepath_log_exists = filepath_log.is_file()

    for i, n in enumerate(n_qubits):
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
                log_writer.writerow(n_qubits)
                log_writer.writerow(simulation_time)

        results_list.append(results)

        test = scipy.stats.binomtest(results.n_rejected, results.shots)
        intervals[0, i], intervals[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate = get_series(results_list, "rejection_rate")
    circuit_depth = get_series(results_list, "circuit_depth")
    n_erasable_gates = get_series(results_list, "n_erasable_gates")
    actual_shots = get_series(results_list, "shots")

    n_accepted = results_list[0].n_accepted
    fidelity = get_series(results_list, "fidelity", n_accepted)

    if plot_error_bars:
        yerr = np.apply_along_axis(lambda row: np.abs(row - rejection_rate), 1, intervals)
    else:
        yerr = None

    p = noise_params.erasure_rate
    rejection_rate_theoretical = 1 - (1 - p)**n_erasable_gates

    with working_directory(FIGURE_DIR):
        fig, ax = plt.subplots()
        ax.errorbar(n_qubits, rejection_rate, yerr, fmt="x-")
        ax.plot(n_qubits, rejection_rate_theoretical, "--", color="grey")
        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("Rejection rate")
        if draw_grid:
            ax.grid()
        save_figure(fig, "rejection-rate-vs-n")

        # TODO: Error bars for total shots? Can be calculated from rejection rate error bars?
        fig, ax = plt.subplots()
        ax.plot(n_qubits, actual_shots, "x-")
        ax.set_yscale("log")
        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("Total shots")
        if draw_grid:
            ax.grid()
        save_figure(fig, "total-shots-vs-n")

        fig, ax = plt.subplots()
        ax.plot(n_qubits, actual_shots / n_accepted, "x-")
        ax.set_yscale("log")
        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel(f"Total shots / target shots({n_accepted})")
        if draw_grid:
            ax.grid()
        save_figure(fig, "total-shots-proportion-vs-n")

        fig, ax = plt.subplots()
        ax.errorbar(circuit_depth, rejection_rate, yerr, fmt="x-")
        ax.plot(circuit_depth, rejection_rate_theoretical, "--", color="grey")
        ax.set_xlabel("Circuit depth")
        ax.set_ylabel("Rejection rate")
        if draw_grid:
            ax.grid()
        save_figure(fig, "rejection-rate-vs-depth")

        fig, ax = plt.subplots()
        ax.plot(n_qubits, circuit_depth, "x-")
        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("Circuit depth")
        if draw_grid:
            ax.grid()
        save_figure(fig, "depth-vs-n")

        fig, ax = plt.subplots()
        ax.plot(n_qubits, n_erasable_gates, "x-")
        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("Number of (erasable) gates, g")
        if draw_grid:
            ax.grid()
        save_figure(fig, "g-vs-n")

        fig, ax = plt.subplots()
        ax.errorbar(n_erasable_gates, rejection_rate, yerr, fmt="x-")
        ax.plot(n_erasable_gates, rejection_rate_theoretical, "--", color="grey")
        ax.set_xlabel("Number of (erasable) gates, g")
        ax.set_ylabel("Rejection rate")
        if draw_grid:
            ax.grid()
        save_figure(fig, "rejection-rate-vs-g")


        mean_fidelity = np.mean(fidelity, axis=1)
        max_fidelity = np.max(fidelity, axis=1)
        min_fidelity = np.min(fidelity, axis=1)

        fig, ax = plt.subplots()
        ax.plot(n_qubits, mean_fidelity, "x-", label="mean")
        ax.plot(n_qubits, max_fidelity, "x-", label="max")
        ax.plot(n_qubits, min_fidelity, "x-", label="min")
        ax.legend()
        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("Fidelity")
        if draw_grid:
            ax.grid()
        save_figure(fig, "fidelity-vs-n")


def plot_ideal_v_noisy(
        plot_error_bars=True,
        draw_grid=True,
    ):
    n_qubits = np.array(range(2, 17))

    # Load ideal data
    results_list_ideal = list[ErasureSimResults]()
    intervals_ideal = np.zeros((2, len(n_qubits)))
    for i, n in enumerate(n_qubits):
        filepath = Path("ideal") / f"qft_sweep_n{n}.json"
        with open(filepath, "rb") as file:
            results = ErasureSimResults.model_validate_json(file.read())

        results_list_ideal.append(results)

        test = scipy.stats.binomtest(results.n_rejected, results.shots)
        intervals_ideal[0, i], intervals_ideal[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate_ideal = get_series(results_list_ideal, "rejection_rate")
    circuit_depth = get_series(results_list_ideal, "circuit_depth")
    n_erasable_gates = get_series(results_list_ideal, "n_erasable_gates")

    # Load noisy data
    # (assumes circuit_depth and n_erasable_gates are the same)
    results_list_noisy = list[ErasureSimResults]()
    intervals_noisy = np.zeros((2, len(n_qubits)))
    for i, n in enumerate(n_qubits):
        filepath = Path("noisy") / f"qft_sweep_n{n}.json"
        with open(filepath, "rb") as file:
            results = ErasureSimResults.model_validate_json(file.read())

        results_list_noisy.append(results)

        test = scipy.stats.binomtest(results.n_rejected, results.shots)
        intervals_noisy[0, i], intervals_noisy[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate_noisy = get_series(results_list_noisy, "rejection_rate")

    # Load noisy data (noisy checks + circ)
    # (assumes circuit_depth and n_erasable_gates are the same)
    results_list_noisy_circ = list[ErasureSimResults]()
    intervals_noisy_circ = np.zeros((2, len(n_qubits)))
    for i, n in enumerate(n_qubits):
        filepath = Path("noisy-circ") / f"qft_sweep_n{n}.json"
        with open(filepath, "rb") as file:
            results = ErasureSimResults.model_validate_json(file.read())

        results_list_noisy_circ.append(results)

        test = scipy.stats.binomtest(results.n_rejected, results.shots)
        intervals_noisy_circ[0, i], intervals_noisy_circ[1, i] = test.proportion_ci()  # defaults to Clopper-Pearson exact method

    rejection_rate_noisy_circ = get_series(results_list_noisy_circ, "rejection_rate")

    if plot_error_bars:
        yerr_ideal = np.apply_along_axis(lambda row: np.abs(row - rejection_rate_ideal), 1, intervals_ideal)
        yerr_noisy = np.apply_along_axis(lambda row: np.abs(row - rejection_rate_noisy), 1, intervals_noisy)
        yerr_noisy_circ = np.apply_along_axis(lambda row: np.abs(row - rejection_rate_noisy_circ), 1, intervals_noisy_circ)
    else:
        yerr_ideal = None
        yerr_noisy = None
        yerr_noisy_circ = None

    p = 0.01
    rejection_rate_theoretical = 1 - (1 - p)**n_erasable_gates

    def plot(ax: Axes, xdata, xlabel):
        noisy_circ = ax.errorbar(xdata, rejection_rate_noisy_circ, yerr_noisy_circ, fmt="x-", label="noisy checks + circuit (depolarising 0.001+0.01)")
        noisy = ax.errorbar(xdata, rejection_rate_noisy, yerr_noisy, fmt="x-", label="noisy checks (falsepos = falseneg = 0.005)")
        ideal = ax.errorbar(xdata, rejection_rate_ideal, yerr_ideal, fmt="x-", label="ideal checks")
        theoretical = ax.plot(xdata, rejection_rate_theoretical, "--", color="gray", label="ideal checks (theoretical)")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Rejection rate")
        ax.set_title(f"QFT (linear connectivity) postselection, erasure rate {p}")

        if draw_grid:
            ax.grid()

        # Customise order of items in legend
        ax.legend(handles=[noisy_circ, noisy, ideal, theoretical[0]])

    # TODO: total shots (+ proportion) in same vein as above

    with working_directory(FIGURE_DIR):
        fig, ax = plt.subplots()
        plot(ax, n_qubits, "Number of qubits, n")
        save_figure(fig, "rejection-rate-comparison-vs-n")

        fig, ax = plt.subplots()
        plot(ax, circuit_depth, "Circuit depth")
        save_figure(fig, "rejection-rate-comparison-vs-depth")

        fig, ax = plt.subplots()
        plot(ax, n_erasable_gates, "Number of (erasable) gates, g")
        save_figure(fig, "rejection-rate-comparison-vs-g")


def plot_times():
    def plot(ax: Axes):
        for filepath in sorted(Path(".").glob("*.csv")):
            with open(filepath, "r") as file:
                file_reader = csv.reader(file)
                n_qubits = np.array(next(file_reader), dtype=int)
                time = np.array(next(file_reader), dtype=float)

            point_style = "x" if "cpu" in filepath.stem else "."
            line_style = "-" if "sampler" in filepath.stem else "--"
            fmt = point_style + line_style
            label = filepath.stem.replace("log-", "")

            ax.plot(n_qubits, time, fmt, label=f"{label} ({sum(time)})")

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


def plot_fidelities(
        plot_as_error: bool = False,
        confidence_level: float | None = 0.95,
        draw_grid: bool = True,
    ):
    n_qubits = np.array(range(2, 17))

    subdirs = [p for p in Path(".").iterdir()
               if p.is_dir()]

    def plot(ax: Axes, component_1: str, component_2: str):
        for dir in subdirs:
            name = dir.name.split("-")

            if name[0] == component_1 and name[1] == component_2:
                results_list = list[ErasureSimResults]()
                for n in n_qubits:
                    # TODO: Standardise above around this directory structure as much as possible.
                    filepath = dir / "data" / f"qft_sweep_n{n}.json"
                    with open(filepath, "rb") as file:
                        results = ErasureSimResults.model_validate_json(file.read())
                    results_list.append(results)

                n_accepted = results_list[0].n_accepted
                fidelity = get_series(results_list, "fidelity", n_accepted)
                if plot_as_error:
                    fidelity = 1 - fidelity

                mean_fidelity = np.mean(fidelity, axis=1)
                min_fidelity = np.max(fidelity, axis=1) if plot_as_error else np.min(fidelity, axis=1)

                if confidence_level is not None:
                    # Calculate error bars for mean via Student's t distribution with standard error of the mean (SEM)
                    n_samples = np.size(fidelity, 1)
                    sem_fidelity = scipy.stats.sem(fidelity, axis=1)
                    yerr = scipy.stats.t.interval(confidence_level, n_samples - 1, loc=mean_fidelity, scale=sem_fidelity)

                    for i in [0, 1]:
                        for j, x in enumerate(yerr[i]):
                            # Resolve NaNs as zero-width intervals
                            if np.isnan(x):
                                yerr[i][j] = mean_fidelity[j]

                            # Convert absolute to relative
                            yerr[i][j] = np.abs(x - mean_fidelity[j])
                else:
                    yerr = None

                colour = "tab:blue" if name[2] == "nopostselect" else "tab:orange"
                ax.errorbar(n_qubits, mean_fidelity, yerr, fmt="x-", label=name[2], color=colour)
                ax.plot(n_qubits, min_fidelity, "x--", color=colour)

        ax.set_xlabel("Number of qubits, n")
        ax.set_ylabel("1 - fidelity" if plot_as_error else "Fidelity")

        ax.set_ylim(-0.05, 1.05)
        # ax.set_yscale("log")

        if draw_grid:
            ax.grid()

        ax.legend()

    fig, ax = plt.subplots()
    component_1, component_2 = "idealchecks", "idealcirc"
    plot(ax, component_1, component_2)
    with working_directory(FIGURE_DIR):
        save_figure(fig, f"fidelity-{component_1}-{component_2}")

    fig, ax = plt.subplots()
    component_1, component_2 = "noisychecks", "idealcirc"
    plot(ax, component_1, component_2)
    with working_directory(FIGURE_DIR):
        save_figure(fig, f"fidelity-{component_1}-{component_2}")

    fig, ax = plt.subplots()
    component_1, component_2 = "noisychecks", "noisycirc"
    plot(ax, component_1, component_2)
    with working_directory(FIGURE_DIR):
        save_figure(fig, f"fidelity-{component_1}-{component_2}")


if __name__ == "__main__":
    matplotlib.rcParams["savefig.dpi"] = 300
    matplotlib.rcParams["savefig.bbox"] = "tight"

    # Configure logging
    import logging
    FORMAT = "[%(filename)11s:%(lineno)3s %(funcName)20s()] %(message)s"
    logging.basicConfig(format=FORMAT)

    logger = logging.getLogger("erado")
    logger.setLevel(logging.DEBUG)

    # Delete data for fresh simulation
    if DELETE_DATA and ROOT_DIR.exists():
        from collections.abc import Generator
        def all_files(p: Path) -> Generator[Path]:
            for child in p.iterdir():
                if child.is_dir():
                    yield from all_files(child)
                else:
                    yield child
        def all_dirs(p: Path) -> Generator[Path]:
            for child in p.iterdir():
                if child.is_dir():
                    yield from all_dirs(child)
                    yield child

        for file in all_files(ROOT_DIR):
            file.unlink()
        for dir in all_dirs(ROOT_DIR):
            dir.rmdir()
        ROOT_DIR.rmdir()

    with working_directory(ROOT_DIR):
        # example_QFT()
        example_QFT_sweep()
        # plot_ideal_v_noisy()
        # plot_times()
        # plot_fidelities()
