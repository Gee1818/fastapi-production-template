from collections.abc import Generator
from pathlib import Path

import pytest
from dependency_injector.wiring import Provide, inject

from app.services.training import TrainingService
from app.settings import Settings
from tests.fixtures.chess_data import get_invalid_elo_data, get_valid_chess_data


@pytest.fixture
def model_path() -> Generator[Path]:
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
    training_service_.model_path = model_path
    return training_service_


@pytest.fixture
def valid_chess_data() -> str:
    return get_valid_chess_data()


@pytest.fixture
def invalid_elo_data() -> str:
    return get_invalid_elo_data()
