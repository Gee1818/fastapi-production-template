import io
from collections.abc import Sequence
from pathlib import Path

import polars as pl
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline  # pyright: ignore[reportUnknownVariableType]
from sklearn.preprocessing import StandardScaler

from app.domain import MLModel
from app.services.helper import load_model, save_model
from app.settings import Settings

from .exceptions import DimensionalityMismatchError


class TrainingService(BaseModel):
    model_path: Path = Field(default=Settings.MODEL_PATH)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def model(self) -> MLModel:
        if self.model_path.exists():
            model = load_model(self.model_path)
            if model:
                return model

        return make_pipeline(StandardScaler(), LogisticRegression())  # type: ignore[return-value]

    @staticmethod
    def prepare_data(file: UploadFile) -> tuple[list[dict[int, int]], list[int]]:
        """This function prepares the data for training.
        It reads the uploaded CSV file, processes it using Polars,
        and returns features and labels for training.
        Args:
            file (UploadFile): The uploaded CSV file.
        Returns:
            tuple[list[dict[str, float]], list[str]]: Features and labels for training.
        """

        contents = file.file.read()

        df = pl.read_csv(io.BytesIO(contents))
        X = df.select(["whiteElo", "blackElo"]).to_dicts()
        y = df["result"].to_list()
        return X, y  # type: ignore[return-value]

    def train(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> MLModel:
        if len(X) != len(y):
            raise DimensionalityMismatchError(x_dim=len(X), y_dim=len(y))

        pipeline = self.model
        pipeline_fit = pipeline.fit(X, y)
        save_model(pipeline_fit, self.model_path)
        return pipeline
