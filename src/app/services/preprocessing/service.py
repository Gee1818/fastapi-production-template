import logging

from fastapi import UploadFile
from pandera.errors import SchemaError
from pydantic import BaseModel, ConfigDict

from app.domain.chess_game import ChessGameSchema
from app.domain.preprocessing.config import (
    FeatureEngineerConfig,
    FilterConfig,
    MappingConfig,
    SelectionConfig,
)
from app.domain.preprocessing.schemas import PreprocessingResult
from app.domain.preprocessing.steps import save_to_csv
from app.domain.preprocessing.steps.feature_engineer import add_features
from app.domain.preprocessing.steps.feature_selection import select_features
from app.domain.preprocessing.steps.filter import apply_filters
from app.domain.preprocessing.steps.mapping import apply_mappings_features
from app.domain.preprocessing.steps.parse_df import read_file
from app.services.exceptions import DataValidationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)


class PreprocessingService(BaseModel):
    filter_config: FilterConfig
    mapping_config: MappingConfig
    feature_engineer_config: FeatureEngineerConfig
    selection_config: SelectionConfig

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def process_file(self, file: UploadFile) -> PreprocessingResult:
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
        df = apply_filters(df, self.filter_config)

        logger.info("Applying mappings")
        df = apply_mappings_features(df, self.mapping_config)

        logger.info("Adding features")
        df = add_features(df, self.feature_engineer_config)

        logger.info("Selecting features")
        df, result = select_features(df, self.selection_config)

        logger.info("Saving processed data to CSV")
        save_to_csv(df)

        logger.info("Preprocessing pipeline completed successfully")

        return result
