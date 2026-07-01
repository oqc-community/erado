# erado

Simulation suite for erasure noise and postselection as quantum error mitigation.

[![build](https://github.com/oqc-community/erado/actions/workflows/build.yaml/badge.svg)](https://github.com/oqc-community/erado/actions/workflows/build.yaml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![PyPI - Version](https://img.shields.io/pypi/v/erado?logo=pypi&label=PyPI)](https://pypi.org/project/erado/) [![docs](https://img.shields.io/badge/Sphinx-docs-orange?logo=sphinx)](https://oqc-community.github.io/erado) [![GitHub License](https://img.shields.io/github/license/oqc-community/erado?logo=spdx)](https://github.com/oqc-community/erado/blob/main/LICENSE)

[**ērādō**](https://en.wiktionary.org/wiki/erado) \
Latin verb; *third conjugation*

1. to scrape away, pare
2. to abolish, eradicate, remove
3. to ***erase***, delete

## Overview

[`erado`](https://github.com/oqc-community/erado) is [OQC](https://oqc.tech/)'s [Qiskit](https://github.com/Qiskit/qiskit)-based Python library for the simulation of circuit-level erasure noise and postselection, with arbitrary quantum circuits.

For a conceptual introduction, usage instructions and API reference, please see [the library documentation](https://oqc-community.github.io/erado/latest/getting-started).

For theoretical background and numerical details, see our corresponding paper: ['The limits of erasure-based postselection for quantum error mitigation,' 2026, arXiv:2606.31428 [quant-ph]](https://arxiv.org/abs/2606.31428), by [Sam J. Griffiths](https://github.com/sgriffiths-oqc), [Jamie Friel](https://github.com/jfriel-oqc) and [Brian Vlastakis](https://github.com/bvlastakis-oqc).

If using or referencing this work, please cite the paper as follows ([BibLaTeX](https://ctan.org/pkg/biblatex)):

```bibtex
@online{griffithsLimitsErasurebasedPostselection2026,
  title = {The Limits of Erasure-Based Postselection for Quantum Error Mitigation},
  author = {Griffiths, Sam J. and Friel, Jamie and Vlastakis, Brian},
  date = {2026-06-30},
  eprint = {2606.31428},
  eprinttype = {arXiv},
  eprintclass = {quant-ph},
  doi = {10.48550/arXiv.2606.31428},
  url = {https://arxiv.org/abs/2606.31428},
  pubstate = {prepublished}
}
```

## Installation

### Published package

The `erado` Python package is published to PyPI (<https://pypi.org/project/erado>), so you can install it easily via pip (or any similar package manager), e.g.:

```shell
pip install erado
```

or add it as a dependency in your `pyproject.toml` file (automatically or manually) if using a package manager such as uv or Poetry, e.g.:

```shell
uv add erado
```

> ⚠️ **NOTE:**
>
> GPU capabilities are provided by the [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) package, which is only available on x86_64 Linux. Therefore, [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) will be installed if `sys.platform() == "linux"`, otherwise [`qiskit-aer`](https://pypi.org/project/qiskit-aer/) will be installed (i.e. if on Windows etc.).

### From source (uv)

This package uses [uv](https://docs.astral.sh/uv) for Python project management. For more information on installation from source and development/testing utilities, please see our [contribution guidelines](./CONTRIBUTING.md).

## Example usage

A motivating example for a simulation running a Qiskit circuit with erasure noise, imperfect erasure checks and postselection (including per-shot circuit fidelity) is as follows:

```python
from erado import (
    circuits,
    models,
    fidelity,
    frontend,
)

import qiskit_aer


n_qubits = 5
circuit = circuits.qft_linear(n_qubits)
circuit.save_statevector(label=fidelity.STATE_LABEL, pershot=True)
circuit.measure_all()

erasure_model = models.ErasureCircuitSampler(
    circuit=circuit,
    erasure_rate=0.01,
)

backend = qiskit_aer.AerSimulator(method="statevector")

sim_frontend = frontend.ErasureSimFrontend(
    model=erasure_model,
    false_positive_rate=0.005,
    false_negative_rate=0.010,
)

results = sim_frontend.run(
    backend=backend,
    shots=1000,
    postselect=True,
    get_fidelities=True,
)
```

For a more detailed introduction as to how and why to use this library, see our ['Getting Started'](https://oqc-community.github.io/erado/latest/getting-started) page.

## Acknowledgements

This work was supported by the Innovate UK Quantum Missions pilot competition 10148061 DECIDE: Dimon error correction integrated into a data-centre environment.
