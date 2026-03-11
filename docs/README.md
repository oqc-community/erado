# erado

Simulation suite for erasure noise and postselection as quantum error mitigation.

[![build](https://github.com/oqc-community/erado/actions/workflows/build.yaml/badge.svg)](https://github.com/oqc-community/erado/actions/workflows/build.yaml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![PyPI - Version](https://img.shields.io/pypi/v/erado?logo=pypi&label=PyPI)](https://pypi.org/project/erado/) [![docs](https://img.shields.io/badge/Sphinx-docs-orange?logo=sphinx)](https://oqc-community.github.io/erado)

[**ērādō**](https://en.wiktionary.org/wiki/erado) \
Latin verb; *third conjugation*

1. to scrape away, pare
2. to abolish, eradicate, remove
3. to ***erase***, delete

## Overview

[`erado`](https://github.com/oqc-community/erado) is [OQC](https://oqc.tech/)'s [Qiskit](https://github.com/Qiskit/qiskit)-based Python library for the simulation of circuit-level erasure noise and postselection, with arbitrary quantum circuits.

For a conceptual introduction, usage instructions and API reference, please see [the library documentation](https://oqc-community.github.io/erado/latest/getting-started).

For theoretical background and numerical details, see our corresponding paper: *coming very soon!*

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
> GPU capabilities are provided by the [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) package, which is only available on x86_64 Linux. Therefore, `qiskit-aer-gpu-cu11` will be installed if `sys.platform() == "linux"`, otherwise `qiskit-aer` will be installed (i.e. if on Windows etc.).

### From source (uv)

This package uses [uv](https://docs.astral.sh/uv) for Python project management. For more information on installation from source and development/testing utilities, please see our [contribution guidelines](./CONTRIBUTING.md).

## Usage

*TODO: brief, simplest example(s).*

For a more detailed introduction to how and why to use this library, see our ['Getting Started'](https://oqc-community.github.io/erado/latest/getting-started) page.

## Acknowledgements

This work was supported by the Innovate UK Quantum Missions pilot competition 10148061 DECIDE: Dimon error correction integrated into a data-centre environment.
