# erado
Simulation suite for error mitigation via dimon erasure models.

[![build](https://github.com/oqc-tech/erado/actions/workflows/build.yaml/badge.svg)](https://github.com/oqc-tech/erado/actions/workflows/build.yaml)

## Dependencies
GPU capabilities are provided by the [`qiskit-aer-gpu-cu11`](https://pypi.org/project/qiskit-aer-gpu-cu11/) package, which is only available on x86_64 Linux. Therefore, `qiskit-aer-gpu-cu11` will be installed if `sys.platform() == "linux"`, otherwise `qiskit-aer` will be installed (i.e. if on Windows etc.).

## Installation
### From source (Poetry)
To ensure that conditional dependencies work properly, you may need to run the following configuration step once on your system (this depends on your Poetry version: it was [introduced in 2.0.0](https://python-poetry.org/docs/configuration/#installerre-resolve) and is [likely to become the default in future Poetry versions](https://python-poetry.org/docs/dependency-specification/#exclusive-extras)):

```shell
poetry config installer.re-resolve false
```

After which the project can be installed in a new virtual environment simply via

```shell
poetry install
```
