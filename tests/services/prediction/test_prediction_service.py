import pytest

from app.domain import PredictionInput
from app.services.prediction import NoTrainedModelError, PredictionService


def test_model_property_returns_none_when_no_model_exists(
    prediction_service: PredictionService,
) -> None:
    """Test that model property returns None when no trained model exists."""
    assert prediction_service.model is None


def test_predict_raises_error_when_no_model(
    prediction_service: PredictionService,
) -> None:
    prediction_input = PredictionInput(age=25.0)

    with pytest.raises(NoTrainedModelError) as exc_info:
        prediction_service.predict(prediction_input)

    assert exc_info.value.message == (
        "No trained model found. Please train the model before making predictions."
    )
