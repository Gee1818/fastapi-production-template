import io
from pathlib import Path

import joblib
import polars as pl
from fastapi import UploadFile
from pandera.errors import SchemaError

from app.domain.chess_game import ChessGameSchema
from app.domain.ml_model import MLModel
from app.services.exceptions import DataValidationError


def load_model(model_path: Path) -> MLModel | None:
    if not model_path.exists():
        return None

    return joblib.load(model_path)  # type: ignore[no-any-return]


def save_model(model: MLModel, model_path: Path) -> None:
    joblib.dump(model, model_path)


def get_feats_and_target(file: UploadFile) -> tuple[pl.DataFrame, pl.Series]:
    contents = file.file.read()
    df = pl.read_csv(io.BytesIO(contents))

    # Validate the DataFrame
    try:
        ChessGameSchema.validate(df)
    except SchemaError as e:
        # Re-raise as HTTP exception for API
        raise DataValidationError(message=f"Data validation failed: {e!s}") from e

    X = df.select(["whiteElo", "blackElo"])
    y = df["result"]

    return X, y
