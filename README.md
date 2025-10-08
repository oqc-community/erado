# erado
Simulation suite for error mitigation via dimon erasure models.

## Installation
### From source (Poetry)
First, to ensure that conditional dependencies work properly, you may need to run the following configuration step once on your system (this depends on your Poetry version: it was [introduced in 2.0.0](https://python-poetry.org/docs/configuration/#installerre-resolve) and is [likely to become the default in future Poetry versions](https://python-poetry.org/docs/dependency-specification/#exclusive-extras)):

```shell
poetry config installer.re-resolve false
```

To install with qiskit-aer GPU capabilities enabled (Linux-only) run:

```shell
poetry install -E gpu
```

Otherwise, the standard ```poetry install``` will install only standard CPU capabilities.
