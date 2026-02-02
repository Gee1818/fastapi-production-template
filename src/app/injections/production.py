from dependency_injector import containers, providers

from app.domain.preprocessing.config import (
    FeatureEngineerConfig,
    FilterConfig,
    MappingConfig,
    SelectionConfig,
)
from app.services import (
    PredictionService,
    ReadFileService,
    TrainingService,
)


class Container(containers.DeclarativeContainer):
    # Configuration providers
    filter_config = providers.Factory(FilterConfig)
    mapping_config = providers.Factory(MappingConfig)
    feature_engineer_config = providers.Factory(FeatureEngineerConfig)
    selection_config = providers.Factory(SelectionConfig)

    prediction_service = providers.Factory(PredictionService)
    training_service = providers.Factory(TrainingService)
    read_file_service = providers.Factory(ReadFileService)
