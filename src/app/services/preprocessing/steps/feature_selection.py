import polars as pl

from app.services.preprocessing.config.feature_selection_config import SelectionConfig


def select_features(
    df: pl.DataFrame, config: SelectionConfig
) -> tuple[pl.DataFrame, pl.Series]:
    X = df.drop(config.features_to_drop)
    y = df[config.target_feature]
    return X, y
