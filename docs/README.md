# erado

Simulation suite for error mitigation via dimon erasure models.

[![build](https://github.com/oqc-tech/erado/actions/workflows/build.yaml/badge.svg)](https://github.com/oqc-tech/erado/actions/workflows/build.yaml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![OQC PyPI](https://img.shields.io/badge/OQC%20PyPI-latest-cornflowerblue?logo=pypi)](https://pypi.int.oqc.app/simple/erado) [![docs](https://img.shields.io/badge/Sphinx-docs-orange?logo=sphinx)](https://oqc-tech.github.io/erado)

[**ērādō**](https://en.wiktionary.org/wiki/erado) \
Latin verb; *third conjugation*

1. to scrape away, pare
2. to abolish, eradicate, remove
3. to ***erase***, delete

## Overview

`erado` is [OQC](https://oqc.tech/)'s [Qiskit](https://github.com/Qiskit/qiskit)-based library for the simulation of circuit-level erasure noise and postselection, with arbitrary quantum circuits.

For installation/usage instructions and API reference, [please see the library documentation](https://oqc-tech.github.io/erado).

<!-- TODO: Update links/authors etc. below. -->

For theoretical background and numerical details, see our corresponding paper: ['The limits of erasure-based postselection for quantum error mitigation,' 2026, arXiv:xxxx.xxxx [quant-ph]](https://arxiv.org/abs/0000.00000), written by [Sam J. Griffiths](https://github.com/sgriffiths-oqc), [Jamie Friel](https://github.com/jfriel-oqc) and [Brian Vlastakis](https://github.com/bvlastakis-oqc).

If using or referencing this work, please cite the paper as follows ([BibLaTeX](https://ctan.org/pkg/biblatex)):

```bibtex
@online{griffithsLimitsErasurebasedPostselection2026,
  title = {The Limits of Erasure-Based Postselection for Quantum Error Mitigation},
  author = {Griffiths, Sam J. and Friel, Jamie and Vlastakis, Brian},
  date = {2026-03-07},
  eprint = {0000.00000},
  eprinttype = {arXiv},
  eprintclass = {quant-ph},
  doi = {00.00000/arXiv.0000.00000},
  url = {https://arxiv.org/abs/0000.00000},
  pubstate = {prepublished}
}
```

## Installation

### Published package

This package is published to our internal PyPI (<https://pypi.int.oqc.app/simple/>) and so, assuming you have access to this source, you can install the latest version thus:

```shell
pip install erado -i https://pypi.int.oqc.app/simple
```

or set it up as an additional dependency source in your `pyproject.toml` file (e.g. if using uv/Poetry).

> ⚠️ **NOTE:**
> GPU capabilities are provided by the [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) package, which is only available on x86_64 Linux. Therefore, `qiskit-aer-gpu-cu11` will be installed if `sys.platform() == "linux"`, otherwise `qiskit-aer` will be installed (i.e. if on Windows etc.).

### From source (uv)

This package uses [uv](https://docs.astral.sh/uv) for Python project management; so, after cloning the repo, you can explicitly configure the project in a fresh virtual environment with

```shell
uv sync
```

This repo uses [pre-commit hooks](https://github.com/pre-commit/pre-commit) to ensure basic code quality (e.g. whitespace, line endings etc.); if you intend to contribute after cloning, it's best to set up pre-commits (to avoid failing PR checks) once with

```shell
uv run pre-commit install
```

Pre-commit hooks automatically check against changed files only. If you want to manually invoke the pre-commit rules on all files in the repo (although, by design, you generally won't need to do that), simply run

```shell
uv run poe pre-commit
```

The [`poe`](https://poethepoet.natn.io/index.html) command can also be used to run other common tasks. For example, all codebase checks (i.e. [linting (Ruff)](https://docs.astral.sh/ruff), [static type checking (Pyright)](https://github.com/microsoft/pyright) and [unit tests (pytest)](https://docs.pytest.org/en/stable)) can be performed with

```shell
uv run poe checks
```

This codebase broadly follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), with some variations. Specific rule definitions can be found in [pyproject.toml](../pyproject.toml).

<!-- TODO: Acknowledgements section at bottom, if necessary? -->
