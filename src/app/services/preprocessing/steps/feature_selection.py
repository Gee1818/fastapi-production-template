import polars as pl

from app.services.preprocessing.config.feature_selection_config import SelectionConfig
from app.settings import Settings


def select_features(df: pl.DataFrame, config: SelectionConfig) -> str:
    df = df.drop(config.features_to_drop)
    save_path = Settings.UPLOAD_DIRECTORY / "train.csv"
    df.write_csv(save_path)

    return save_path
