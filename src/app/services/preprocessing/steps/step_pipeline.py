import polars as pl
from fastapi import UploadFile

from app.services.preprocessing.config.feature_engineer_config import (
    FeatureEngineerConfig,
)
from app.services.preprocessing.config.feature_selection_config import (
    SelectionConfig,
)
from app.services.preprocessing.config.filter_config import FilterConfig
from app.services.preprocessing.config.mapping_config import MappingConfig

from .feature_engineer import FeatureEngineer
from .feature_selection import FeatureSelector
from .filter import GameFilter
from .mapping import GameMapping
from .parse_df import ConvertToDf


class PreprocessingPipeline:
    @staticmethod
    def run_pipeline(
        file: UploadFile,
        filter_config: FilterConfig,
        mapping_config: MappingConfig,
        feature_engineer_config: FeatureEngineerConfig,
        selection_config: SelectionConfig,
    ) -> tuple[pl.DataFrame, pl.Series]:
        df = ConvertToDf.read_file(file)
        df = GameFilter.apply_filters(df, filter_config)
        df = GameMapping.apply_mappings(df, mapping_config)
        df = FeatureEngineer.add_features(df, feature_engineer_config)
        X, y = FeatureSelector.select_features(df, selection_config)
        return X, y
