from pathlib import Path

from fastapi import UploadFile
from joblib import Memory
from pydantic import BaseModel, ConfigDict, Field
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline  # pyright: ignore[reportUnknownVariableType]
from sklearn.preprocessing import StandardScaler

from app.domain.ml_model import MLModel
from app.services.helper import load_model, save_model
from app.services.preprocessing.config.config import (
    feature_engineer_config,
    filter_config,
    mapping_config,
    selection_config,
)
from app.services.preprocessing.steps.step_pipeline import run_pipeline
from app.settings import Settings


class TrainingService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def model(self) -> MLModel:
        if self.model_path.exists():
            model = load_model(self.model_path)
            if model:
                return model

        memory = Memory(location=".pipe_cache", verbose=0)

        return make_pipeline(StandardScaler(), LogisticRegression(), memory=memory)

    def train(self, file: UploadFile) -> MLModel:
        X, y = run_pipeline(
            file=file,
            filter_config=filter_config,
            mapping_config=mapping_config,
            feature_engineer_config=feature_engineer_config,
            selection_config=selection_config,
        )

        pipeline = self.model
        pipeline_fit = pipeline.fit(X, y)
        save_model(pipeline_fit, self.model_path)
        return pipeline
