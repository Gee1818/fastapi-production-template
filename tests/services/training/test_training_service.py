import pytest

from app.services.exceptions import DataValidationError
from app.services.training import TrainingService
from app.settings import Settings


def test_train_with_invalid_elo(
    training_service: TrainingService,
    invalid_elo_data: str,
) -> None:
    """Test that training with invalid ELO raises validation error."""
    # Create the training file with invalid data
    training_file = Settings.UPLOAD_DIRECTORY / "train.pgn"
    training_file.write_text(invalid_elo_data)

    try:
        with pytest.raises(DataValidationError):
            training_service.train()
    finally:
        # Clean up
        training_file.unlink(missing_ok=True)


def test_train_with_valid_data(
    training_service: TrainingService,
    valid_chess_data: str,
) -> None:
    """Test that training with valid data succeeds."""
    # Create the training file with valid data
    training_file = Settings.UPLOAD_DIRECTORY / "train.pgn"
    training_file.write_text(valid_chess_data)

    try:
        model = training_service.train()

        # Verify model was created and saved
        assert model is not None
        assert training_service.model_path.exists()
    finally:
        # Clean up
        training_file.unlink(missing_ok=True)


def test_train_raises_error_when_file_not_found(
    training_service: TrainingService,
) -> None:
    """Test that training raises FileNotFoundError when train.pgn doesn't exist."""
    # Ensure the file doesn't exist
    training_file = Settings.UPLOAD_DIRECTORY / "train.pgn"
    training_file.unlink(missing_ok=True)

    with pytest.raises(FileNotFoundError) as exc_info:
        training_service.train()

    assert "Training file not found" in str(exc_info.value)


def test_train_with_custom_training_file_path(
    training_service: TrainingService,
    valid_chess_data: str,
) -> None:
    """Test that training works with a custom file path."""
    # Create a custom training file
    custom_file = Settings.UPLOAD_DIRECTORY / "custom_train.pgn"
    custom_file.write_text(valid_chess_data)

    # Update the service to use the custom file
    training_service.training_file_path = custom_file

    try:
        model = training_service.train()

        # Verify model was created and saved
        assert model is not None
        assert training_service.model_path.exists()
    finally:
        # Clean up
        custom_file.unlink(missing_ok=True)
