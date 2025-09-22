import io

import pandera as pa
import polars as pl
from fastapi import HTTPException, UploadFile

from app.domain.chess_game import ChessGameSchema


def get_feats_and_target(file: UploadFile) -> tuple[pl.DataFrame, pl.Series]:
    contents = file.file.read()
    df = pl.read_csv(io.BytesIO(contents))

    # Validate the DataFrame
    try:
        ChessGameSchema.validate(df)
    except pa.errors.SchemaError as e:
        # Re-raise as HTTP exception for API
        raise HTTPException(
            status_code=400, detail=f"Data validation failed: {e!s}"
        ) from e

    X = df.select(["whiteElo", "blackElo"])
    y = df["result"]

    return X, y
