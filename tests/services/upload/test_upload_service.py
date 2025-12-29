import io

import polars as pl
import pytest
from fastapi import UploadFile

from app.services.exceptions import DataValidationError
from app.services.upload import UploadService
from app.settings import Settings


def test_save_file_success(
    valid_upload_file: UploadFile,
) -> None:
    """Test successful file upload and processing."""
    # Arrange
    service = UploadService()

    # Act
    result = service.save_file(valid_upload_file)

    # Assert
    assert "message" in result
    assert "totalFeatures" in result
    assert "totalRows" in result

    assert result["message"] == "Feature selection completed"
    assert isinstance(result["totalFeatures"], int)
    assert isinstance(result["totalRows"], int)
    assert result["totalFeatures"] > 0
    assert result["totalRows"] > 0

    # Verify train.csv was created
    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    assert train_file.exists()


def test_save_file_invalid_elo_fails(
    invalid_elo_upload_file: UploadFile,
) -> None:
    """Test that file with invalid ELO ratings raises DataValidationError."""
    # Arrange
    service = UploadService()

    # Act & Assert
    with pytest.raises(DataValidationError) as exc_info:
        service.save_file(invalid_elo_upload_file)

    assert "Data validation failed" in exc_info.value.message
    assert "WhiteElo" in exc_info.value.message or "BlackElo" in exc_info.value.message


def test_save_file_creates_correct_structure(
    valid_upload_file: UploadFile,
) -> None:
    """Test that saved file has correct column structure."""
    # Arrange
    service = UploadService()

    # Act
    service.save_file(valid_upload_file)

    # Assert

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    df = pl.read_csv(train_file)

    # Check for expected columns
    expected_columns = [
        "Event",
        "Result",
        "WhiteElo",
        "BlackElo",
        "ECO",
        "Opening",
        "TimeControl",
        "Termination",
        "white_material",
        "black_material",
        "material_diff",
    ]

    for col in expected_columns:
        assert col in df.columns, f"Column {col} missing from output"

    # Check that filtered columns are not present
    filtered_columns = ["Site", "Date", "Round", "White", "Black", "Moves"]
    for col in filtered_columns:
        assert col not in df.columns, f"Column {col} should be filtered out"


def test_save_file_filters_data_correctly(
    valid_upload_file: UploadFile,
) -> None:
    """Test that file processing applies filters correctly."""
    # Arrange
    service = UploadService()

    # Act
    service.save_file(valid_upload_file)

    # Assert - should have filtered data

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    df = pl.read_csv(train_file)

    # All rows should have valid ELO ratings
    assert df["WhiteElo"].min() >= 1400
    assert df["WhiteElo"].max() <= 2800
    assert df["BlackElo"].min() >= 1400
    assert df["BlackElo"].max() <= 2800

    # All rows should have valid events
    valid_events = ["Blitz", "Rapid", "Classical"]
    assert all(event in valid_events for event in df["Event"].unique())


def test_save_file_empty_after_filtering(
    wrong_event_type_pgn: str,
) -> None:
    """Test handling when all games are filtered out."""

    service = UploadService()
    file_obj = io.BytesIO(wrong_event_type_pgn.encode())
    upload_file = UploadFile(filename="wrong_event.pgn", file=file_obj)

    result = service.save_file(upload_file)

    assert result["totalRows"] == 0
    assert result["totalFeatures"] > 0


def test_save_file_preserves_result_mapping(
    valid_upload_file: UploadFile,
) -> None:
    """Test that result values are properly mapped."""
    # Arrange
    service = UploadService()

    # Act
    service.save_file(valid_upload_file)

    # Assert

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    df = pl.read_csv(train_file)

    # Result should be mapped to -1, 0, 1
    unique_results = df["Result"].unique().sort()
    assert all(result in {-1, 0, 1} for result in unique_results)
