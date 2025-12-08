import logging
from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field

from app.domain import MLModel
from app.services.helper import load_model
from app.services.preprocessing.config.feature_engineer_config import (
    FeatureEngineerConfig,
)
from app.services.preprocessing.config.feature_selection_config import (
    SelectionConfig,
)
from app.services.preprocessing.config.filter_config import FilterConfig
from app.services.preprocessing.config.mapping_config import MappingConfig
from app.services.preprocessing.steps.step_pipeline import run_pipeline
from app.settings import Settings

from .exceptions import NoTrainedModelError

logger = logging.getLogger(__name__)


class PredictionService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    filter_config: FilterConfig = FilterConfig()
    mapping_config: MappingConfig = MappingConfig()
    feature_engineer_config: FeatureEngineerConfig = FeatureEngineerConfig()
    selection_config: SelectionConfig = SelectionConfig()

    @property
    def model(self) -> MLModel | None:
        return load_model(self.model_path)

    def predict(self, file: UploadFile) -> list[float]:
        if self.model is None:
            raise NoTrainedModelError
        X, _ = run_pipeline(
            file=file,
            filter_config=self.filter_config,
            mapping_config=self.mapping_config,
            feature_engineer_config=self.feature_engineer_config,
            selection_config=self.selection_config,
        )
        logger.info("head of preprocessed data: %s", X.head())
        logger.info("Generating predictions")
        predictions = self.model.predict_proba(X)
        logger.info("Predictions generated successfully")
        logger.info("Number of predictions: %s", len(predictions))  # pyright: ignore[reportArgumentType]
        logger.info("Prediction results: %s", predictions)

        return self.model.predict_proba(X)  # pyright: ignore[reportReturnType]
