from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from app.domain import MLModel
from app.services.helper import load_model
from app.settings import Settings


class PredictionService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def model(self) -> MLModel | None:
        return load_model(self.model_path)
