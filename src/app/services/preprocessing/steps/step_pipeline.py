import logging

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

from .feature_engineer import add_features
from .feature_selection import select_features
from .filter import apply_filters
from .mapping import apply_mappings
from .parse_df import read_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,  # This ensures it overrides any existing config
)


def run_pipeline(
    file: UploadFile,
    filter_config: FilterConfig,
    mapping_config: MappingConfig,
    feature_engineer_config: FeatureEngineerConfig,
    selection_config: SelectionConfig,
) -> dict[str, str | int]:
    logger = logging.getLogger(__name__)
    logger.info("Starting preprocessing pipeline")

    logger.info("Reading file")
    df = read_file(file)

    try:
        logger.info("Validating data schema")
        ChessGameSchema.validate(df)
    except SchemaError as e:
        logger.exception("Data validation failed", extra={"error": str(e)})
        raise DataValidationError(message=f"Data validation failed: {e!s}") from e

    logger.info("Applying filters")
    df = apply_filters(df, filter_config)

    logger.info("Applying mappings")
    df = apply_mappings(df, mapping_config)

    logger.info("Adding features")
    df = add_features(df, feature_engineer_config)

    logger.info("Selecting features")
    msg = select_features(df, selection_config)

    logger.info("Preprocessing pipeline completed successfully")
    logger.info("Processed data saved at: %s", msg)
    return msg
