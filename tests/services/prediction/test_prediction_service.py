import io

import pytest
from fastapi import UploadFile

from app.services.prediction import NoTrainedModelError, PredictionService
from app.services.training import TrainingService


def test_model_property_returns_none_when_no_model_exists(
    prediction_service: PredictionService,
) -> None:
    """Test that model property returns None when no trained model exists."""
    assert prediction_service.model is None


def test_model_property_returns_model_when_exists(
    prediction_service: PredictionService,
    valid_chess_data: str,
) -> None:
    """Test that model property returns a model when one exists."""
    # First train a model
    training_service = TrainingService(model_path=prediction_service.model_path)
    file_obj = io.BytesIO(valid_chess_data.encode())
    upload_file = UploadFile(filename="train.csv", file=file_obj)
    training_service.train(upload_file)

    # Now check if model loads
    model = prediction_service.model
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "fit")


def test_predict_raises_error_when_no_model(
    prediction_service: PredictionService,
    valid_chess_data: str,
) -> None:
    """Test that predict raises NoTrainedModelError when no model exists."""
    file_obj = io.BytesIO(valid_chess_data.encode())
    upload_file = UploadFile(filename="test.csv", file=file_obj)

    with pytest.raises(NoTrainedModelError) as exc_info:
        prediction_service.predict(upload_file)

    assert exc_info.value.message == (
        "No trained model found. Please train the model before making predictions."
    )
