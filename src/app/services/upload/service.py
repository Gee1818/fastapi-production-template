from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel

from app.domain.preprocessing.config import (
    FeatureEngineerConfig,
    FilterConfig,
    MappingConfig,
    SelectionConfig,
)
from app.domain.preprocessing.steps import run_pipeline
from app.settings import Settings


class UploadService(BaseModel):
    upload_directory: Path = Settings.UPLOAD_DIRECTORY
    filter_config: FilterConfig = FilterConfig()
    mapping_config: MappingConfig = MappingConfig()
    feature_engineer_config: FeatureEngineerConfig = FeatureEngineerConfig()
    selection_config: SelectionConfig = SelectionConfig()

    def save_file(self, file: UploadFile) -> dict[str, str | int]:

        result = run_pipeline(
            file=file,
            filter_config=self.filter_config,
            mapping_config=self.mapping_config,
            feature_engineer_config=self.feature_engineer_config,
            selection_config=self.selection_config,
        )

        return {
            "message": result.message,
            "totalFeatures": result.total_features,
            "totalRows": result.total_rows,
        }
