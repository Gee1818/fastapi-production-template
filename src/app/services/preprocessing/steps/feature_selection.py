import polars as pl

from app.services.preprocessing.config.feature_selection_config import SelectionConfig


class FeatureSelector:
    @staticmethod
    def select_features(df: pl.DataFrame, config: SelectionConfig) -> pl.DataFrame:
        return df.drop(config.features_to_drop)
