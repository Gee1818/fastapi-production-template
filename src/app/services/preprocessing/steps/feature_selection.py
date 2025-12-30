import polars as pl

from app.services.preprocessing.config.feature_selection_config import SelectionConfig
from app.services.preprocessing.steps.csv_save import csv_save


def select_features(df: pl.DataFrame, config: SelectionConfig) -> dict[str, str | int]:
    df = df.drop(config.features_to_drop)
    csv_save(df)

    return {
        "message": "Feature selection completed",
        "total_features": df.shape[1],
        "total_rows": df.shape[0],
    }
