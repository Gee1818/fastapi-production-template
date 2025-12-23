import pytest

from app.services.training import TrainingService
from app.settings import Settings


def test_train_with_nonexistent_file(
    training_service: TrainingService,
) -> None:
    """Test that training raises FileNotFoundError when training file doesn't exist."""
    # Use a path that doesn't exist
    nonexistent_path = Settings.UPLOAD_DIRECTORY / "nonexistent.csv"

    with pytest.raises(FileNotFoundError) as exc_info:
        training_service.train(nonexistent_path)

    assert f"Training file not found at {nonexistent_path}" in str(exc_info.value)


def test_train_with_valid_csv(
    training_service: TrainingService,
) -> None:
    """Test that training with valid CSV data succeeds."""
    # Use the existing train.csv file from uploads directory
    training_file = Settings.DEFAULT_TRAINING_FILE

    # Only run test if file exists (it should from your documents)
    if not training_file.exists():
        pytest.skip("train.csv not found in uploads directory")

    model = training_service.train(training_file)

    # Verify model was created and saved
    assert model is not None
    assert training_service.model_path.exists()
    assert hasattr(model, "predict")
    assert hasattr(model, "fit")
