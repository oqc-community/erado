# erado

Simulation suite for error mitigation via dimon erasure models.

[![build](https://github.com/oqc-tech/erado/actions/workflows/build.yaml/badge.svg)](https://github.com/oqc-tech/erado/actions/workflows/build.yaml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![OQC PyPI](https://img.shields.io/badge/OQC%20PyPI-latest-cornflowerblue?logo=pypi)](https://pypi.int.oqc.app/simple/erado)

[**ērādō**](https://en.wiktionary.org/wiki/erado) \
Latin verb; *third conjugation*

1. to scrape away, pare
2. to abolish, eradicate, remove
3. to ***erase***, delete

## Dependencies

GPU capabilities are provided by the [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) package, which is only available on x86_64 Linux. Therefore, `qiskit-aer-gpu-cu11` will be installed if `sys.platform() == "linux"`, otherwise `qiskit-aer` will be installed (i.e. if on Windows etc.).

## Installation

### Published package

This package is published to our internal PyPI (<https://pypi.int.oqc.app/simple/>) and so, assuming you have access to this source, you can install the latest version thus:

```shell
pip install erado -i https://pypi.int.oqc.app/simple
```

or set it up as an additional dependency source in your `pyproject.toml` file (e.g. if using uv/Poetry).

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
