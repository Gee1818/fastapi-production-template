from collections.abc import Generator

import pytest

from app.services.upload import UploadService
from app.settings import Settings
from tests.fixtures.chess_data import (
    invalid_elo_pgn,
    valid_pgn_data,
)


@pytest.fixture
def upload_service() -> UploadService:
    return UploadService()


@pytest.fixture
def valid_chess_data() -> str:
    return valid_pgn_data()


@pytest.fixture
def invalid_elo_data() -> str:
    return invalid_elo_pgn()


@pytest.fixture(autouse=True)
def cleanup_train_csv() -> Generator[None, None, None]:
    yield
    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    train_file.unlink(missing_ok=True)
