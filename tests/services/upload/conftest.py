from collections.abc import Generator

import pytest

from app.services.upload import UploadService
from app.settings import Settings
from tests.fixtures.chess_data import get_invalid_elo_data, get_valid_chess_data


@pytest.fixture
def upload_service() -> UploadService:
    return UploadService()


@pytest.fixture
def valid_chess_data() -> str:
    return get_valid_chess_data()


@pytest.fixture
def invalid_elo_data() -> str:
    return get_invalid_elo_data()


@pytest.fixture(autouse=True)
def cleanup_train_csv() -> Generator[None, None, None]:
    yield
    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    train_file.unlink(missing_ok=True)
