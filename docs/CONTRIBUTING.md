# Contributing

*This codebase broadly follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), with some variations. Specific rule definitions can be found in [pyproject.toml](https://github.com/oqc-community/erado/blob/main/pyproject.toml).*

## Installation from source

This package uses [uv](https://docs.astral.sh/uv) for Python project management; after cloning the repo, you can explicitly configure the project in a fresh virtual environment with

```shell
uv sync
```

> ⚠️ **NOTE:**
>
> GPU capabilities are provided by the [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) package, which is only available on x86_64 Linux. Therefore, `qiskit-aer-gpu-cu11` will be installed if `sys.platform() == "linux"`, otherwise [`qiskit-aer`](https://pypi.org/project/qiskit-aer/) will be installed (i.e. if on Windows etc.).

## Pre-commit hooks

This repo uses [pre-commit hooks](https://github.com/pre-commit/pre-commit) to ensure basic code quality (e.g. whitespace, line endings etc.); if you intend to contribute after cloning, it's best to set up pre-commits (to avoid failing PR checks) once with

```shell
uv run pre-commit install
```

Pre-commit hooks automatically check against changed files only. If you want to manually invoke the pre-commit rules on all files in the repo (although, by design, you generally won't need to do that), simply run

```shell
uv run poe pre-commit
```

## Static analysis and unit tests

The [`poe`](https://poethepoet.natn.io/index.html) command can also be used to run other common tasks. For example, all codebase checks (i.e. [linting (Ruff)](https://docs.astral.sh/ruff), [static type checking (Pyright)](https://github.com/microsoft/pyright) and [unit tests (pytest)](https://docs.pytest.org/en/stable)) can be performed with

```shell
uv run poe checks
```

You can consult the output of `uv run poe --help` for more information on other tasks also defined via the `poe` utility.
