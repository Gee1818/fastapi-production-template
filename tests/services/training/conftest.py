"""Fixtures specific to training service tests."""

from collections.abc import Generator
from pathlib import Path

import pytest
from dependency_injector.wiring import Provide, inject

from app.services.training import TrainingService
from app.settings import Settings


@pytest.fixture
def model_path() -> Generator[Path, None, None]:
    """Fixture providing a path for training model files."""
    model_path = Settings.MODEL_DIRECTORY / "model_test.joblib"
    model_path.unlink(missing_ok=True)
    yield model_path
    model_path.unlink(missing_ok=True)


@pytest.fixture
@inject
def training_service(
    model_path: Path,
    training_service_: TrainingService = Provide["training_service"],
) -> TrainingService:
    """Fixture providing a training service with test model path."""
    training_service_.model_path = model_path
    return training_service_
