import polars as pl

from app.services.preprocessing.config.feature_selection_config import SelectionConfig

target_col = SelectionConfig.target_feature


def split_features_target(df: pl.DataFrame) -> tuple[pl.DataFrame, pl.Series]:

    y = df[target_col]
    X = df.drop(target_col)
    return X, y
