from collections.abc import Generator
from pathlib import Path

import pytest
from dependency_injector.wiring import Provide, inject

from app.services.prediction import PredictionService
from app.settings import Settings


@pytest.fixture
def prediction_model_path() -> Generator[Path]:
    model_path = Settings.MODEL_DIRECTORY / "prediction_model_test.joblib"
    model_path.unlink(missing_ok=True)
    yield model_path
    model_path.unlink(missing_ok=True)


@pytest.fixture
@inject
def prediction_service(
    prediction_model_path: Path,
    prediction_service_: PredictionService = Provide["prediction_service"],
) -> PredictionService:
    prediction_service_.model_path = prediction_model_path
    return prediction_service_
