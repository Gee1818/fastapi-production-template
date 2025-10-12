import io

import pytest
from fastapi import UploadFile

from app.services.exceptions import DataValidationError
from app.services.training import TrainingService


def test_train_with_invalid_result(
    training_service: TrainingService,
    invalid_result_data: str,
) -> None:
    file_obj = io.BytesIO(invalid_result_data.encode())
    upload_file = UploadFile(filename="test.csv", file=file_obj)
    with pytest.raises(DataValidationError):
        training_service.train(upload_file)


def test_train_with_invalid_elo(
    training_service: TrainingService,
    invalid_elo_data: str,
) -> None:
    file_obj = io.BytesIO(invalid_elo_data.encode())
    upload_file = UploadFile(filename="test.csv", file=file_obj)
    with pytest.raises(DataValidationError):
        training_service.train(upload_file)


def test_train_with_valid_data(
    training_service: TrainingService,
    valid_chess_data: str,
) -> None:
    file_obj = io.BytesIO(valid_chess_data.encode())
    upload_file = UploadFile(filename="test.csv", file=file_obj)
    training_service.train(upload_file)
