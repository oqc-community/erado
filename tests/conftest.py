"""Main pytest configuration file."""

import erado.models as models

import pytest


MODEL_TYPES: list[type[models.ErasureModel]] = [
    models.ErasureCircuitSampler,
    models.ErasurePassJob,
]


@pytest.fixture(params=MODEL_TYPES)
def model_type(request: pytest.FixtureRequest) -> type[models.ErasureModel]:
    """Parametrise `model_type: type[ErasureModel]` with every `ErasureModel` in `erado`."""
    return request.param
