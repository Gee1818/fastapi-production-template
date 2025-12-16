from dependency_injector import containers, providers

from app.services import PredictionService, TrainingService, UploadService


class Container(containers.DeclarativeContainer):
    prediction_service = providers.Factory(PredictionService)
    training_service = providers.Factory(TrainingService)
    upload_service = providers.Factory(UploadService)
