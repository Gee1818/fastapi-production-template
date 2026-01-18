from dependency_injector import containers, providers

from app.domain.preprocessing.config import (
    FeatureEngineerConfig,
    FilterConfig,
    MappingConfig,
    SelectionConfig,
)
from app.services import PredictionService, TrainingService, UploadService
from app.services.preprocessing.service import PreprocessingService


class Container(containers.DeclarativeContainer):
    # Configuration providers
    filter_config = providers.Factory(FilterConfig)
    mapping_config = providers.Factory(MappingConfig)
    feature_engineer_config = providers.Factory(FeatureEngineerConfig)
    selection_config = providers.Factory(SelectionConfig)

    # Service providers
    preprocessing_service = providers.Factory(
        PreprocessingService,
        filter_config=filter_config,
        mapping_config=mapping_config,
        feature_engineer_config=feature_engineer_config,
        selection_config=selection_config,
    )

    upload_service = providers.Factory(
        UploadService,
        preprocessing_service=preprocessing_service,
    )

    prediction_service = providers.Factory(PredictionService)
    training_service = providers.Factory(TrainingService)
