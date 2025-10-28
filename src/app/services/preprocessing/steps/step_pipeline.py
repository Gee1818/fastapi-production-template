import logging

import polars as pl
from fastapi import UploadFile
from pandera.errors import SchemaError

from app.domain.chess_game import ChessGameSchema
from app.services.exceptions import DataValidationError
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
        logger = logging.getLogger(__name__)
        logger.info("Starting preprocessing pipeline")

        logger.info("Reading file")
        df = ConvertToDf.read_file(file)

        try:
            logger.info("Validating data schema")
            ChessGameSchema.validate(df)
        except SchemaError as e:
            logger.exception(f"Data validation failed: {e!s}")
            raise DataValidationError(message=f"Data validation failed: {e!s}") from e

        logger.info("Applying filters")
        df = GameFilter.apply_filters(df, filter_config)

        logger.info("Applying mappings")
        df = GameMapping.apply_mappings(df, mapping_config)

        logger.info("Adding features")
        df = FeatureEngineer.add_features(df, feature_engineer_config)

        logger.info("Selecting features")
        X, y = FeatureSelector.select_features(df, selection_config)

        logger.info("Preprocessing pipeline completed successfully")
        return X, y
