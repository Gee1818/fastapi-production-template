from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline  # pyright: ignore[reportUnknownVariableType]
from sklearn.preprocessing import StandardScaler

from app.domain.ml_model import MLModel
from app.services.helper import get_feats_and_target, load_model, save_model
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

        return make_pipeline(StandardScaler(), LogisticRegression())

    def train(self, file: UploadFile) -> MLModel:
        X, y = get_feats_and_target(file)

        pipeline = self.model
        pipeline_fit = pipeline.fit(X, y)
        save_model(pipeline_fit, self.model_path)
        return pipeline
