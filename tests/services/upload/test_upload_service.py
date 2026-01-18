import io

import polars as pl
import pytest
from fastapi import UploadFile

from app.domain.preprocessing.config.config import ELO_RANGE
from app.services.exceptions import DataValidationError
from app.services.upload import UploadService
from app.settings import Settings


def test_save_file_success(
    valid_upload_file: UploadFile,
    upload_service: UploadService,
) -> None:
    result = upload_service.save_file(valid_upload_file)

    assert hasattr(result, "message")
    assert hasattr(result, "total_features")
    assert hasattr(result, "total_rows")

    assert result.message == "Feature selection completed"
    assert isinstance(result.total_features, int)
    assert isinstance(result.total_rows, int)
    assert result.total_features > 0
    assert result.total_rows > 0

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    assert train_file.exists()


def test_save_file_invalid_elo_fails(
    invalid_elo_upload_file: UploadFile,
    upload_service: UploadService,
) -> None:
    with pytest.raises(DataValidationError) as exc_info:
        upload_service.save_file(invalid_elo_upload_file)

    assert "Data validation failed" in exc_info.value.message
    assert "WhiteElo" in exc_info.value.message or "BlackElo" in exc_info.value.message


def test_save_file_creates_correct_structure(
    valid_upload_file: UploadFile,
    upload_service: UploadService,
) -> None:
    upload_service.save_file(valid_upload_file)

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    df = pl.read_csv(train_file)

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

    filtered_columns = ["Site", "Date", "Round", "White", "Black", "Moves"]
    for col in filtered_columns:
        assert col not in df.columns, f"Column {col} should be filtered out"


def test_save_file_filters_data_correctly(
    valid_upload_file: UploadFile,
    upload_service: UploadService,
) -> None:
    upload_service.save_file(valid_upload_file)

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    df = pl.read_csv(train_file)

    MIN_ELO, MAX_ELO = ELO_RANGE

    white_elo_min = df["WhiteElo"].min()
    white_elo_max = df["WhiteElo"].max()
    black_elo_min = df["BlackElo"].min()
    black_elo_max = df["BlackElo"].max()

    assert white_elo_min is not None
    assert isinstance(white_elo_min, (int, float))
    assert white_elo_min >= MIN_ELO

    assert white_elo_max is not None
    assert isinstance(white_elo_max, (int, float))
    assert white_elo_max <= MAX_ELO

    assert black_elo_min is not None
    assert isinstance(black_elo_min, (int, float))
    assert black_elo_min >= MIN_ELO

    assert black_elo_max is not None
    assert isinstance(black_elo_max, (int, float))
    assert black_elo_max <= MAX_ELO

    valid_events = ["Blitz", "Rapid", "Classical"]
    assert all(event in valid_events for event in df["Event"].unique())


def test_save_file_empty_after_filtering(
    wrong_event_type_pgn: str,
    upload_service: UploadService,
) -> None:
    file_obj = io.BytesIO(wrong_event_type_pgn.encode())
    upload_file = UploadFile(filename="wrong_event.pgn", file=file_obj)

    result = upload_service.save_file(upload_file)

    assert result.total_rows == 0
    assert int(result.total_features) > 0


def test_save_file_preserves_result_mapping(
    valid_upload_file: UploadFile,
    upload_service: UploadService,
) -> None:
    upload_service.save_file(valid_upload_file)

    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    df = pl.read_csv(train_file)

    unique_results = df["Result"].unique().sort()
    assert all(result in {-1, 0, 1} for result in unique_results)
