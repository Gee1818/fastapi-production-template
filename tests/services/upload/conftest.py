from collections.abc import Generator

import pytest

from app.services.upload import UploadService
from app.settings import Settings


@pytest.fixture
def upload_service() -> UploadService:
    return UploadService()


@pytest.fixture(autouse=True)
def cleanup_train_csv() -> Generator[None]:
    yield
    train_file = Settings.DEFAULT_TRAINING_FILE
    train_file.unlink(missing_ok=True)
