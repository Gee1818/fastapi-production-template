import polars as pl

from app.domain.preprocessing.config import SelectionConfig


def select_features(df: pl.DataFrame, config: SelectionConfig) -> pl.DataFrame:
    return df.drop(config.features_to_drop)
