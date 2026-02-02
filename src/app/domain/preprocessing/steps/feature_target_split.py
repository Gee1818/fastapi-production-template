import polars as pl

from app.domain.preprocessing.config import SelectionConfig


def split_features_target(df: pl.DataFrame) -> tuple[pl.DataFrame, pl.Series]:

    y = df[SelectionConfig.target_feature]
    X = df.drop(SelectionConfig.target_feature)
    return X, y
