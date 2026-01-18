from collections.abc import Generator

import pytest

from app.domain.preprocessing.config import (
    FeatureEngineerConfig,
    FilterConfig,
    MappingConfig,
    SelectionConfig,
)
from app.services.preprocessing import PreprocessingService
from app.services.upload import UploadService
from app.settings import Settings


@pytest.fixture
def upload_service() -> UploadService:
    preprocessing_service = PreprocessingService(
        filter_config=FilterConfig(),
        mapping_config=MappingConfig(),
        feature_engineer_config=FeatureEngineerConfig(),
        selection_config=SelectionConfig(),
    )
    return UploadService(preprocessing_service=preprocessing_service)


@pytest.fixture(autouse=True)
def cleanup_train_csv() -> Generator[None]:
    yield
    train_file = Settings.DEFAULT_TRAINING_FILE
    train_file.unlink(missing_ok=True)
