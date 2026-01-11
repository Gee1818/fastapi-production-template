import polars as pl

from app.domain.preprocessing.config import SelectionConfig
from app.domain.preprocessing.schemas import PreprocessingResult


def select_features(
    df: pl.DataFrame, config: SelectionConfig
) -> tuple[pl.DataFrame, PreprocessingResult]:
    df = df.drop(config.features_to_drop)

    result = PreprocessingResult(
        message="Feature selection completed",
        total_features=df.shape[1],
        total_rows=df.shape[0],
    )

    return df, result
