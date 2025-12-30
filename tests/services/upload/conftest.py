"""Fixtures specific to upload service tests."""

from collections.abc import Generator

import pytest

from app.services.upload import UploadService
from app.settings import Settings


@pytest.fixture
def upload_service() -> UploadService:
    """Fixture providing an upload service instance."""
    return UploadService()


@pytest.fixture(autouse=True)
def cleanup_train_csv() -> Generator[None, None, None]:
    """Cleanup fixture to remove train.csv after tests."""
    yield
    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    train_file.unlink(missing_ok=True)
