from collections.abc import Iterable

from fastapi import APIRouter

from .health import health_router
from .prediction import PredictionRequest, PredictionResponse, prediction_router
from .train import TrainResponse, train_router
from .upload import UploadResponse, upload_router

ROUTERS: Iterable[APIRouter] = (
    health_router,
    prediction_router,
    train_router,
    upload_router,
)

__all__ = [
    "ROUTERS",
    "PredictionRequest",
    "PredictionResponse",
    "TrainResponse",
    "UploadResponse",
    "health_router",
    "prediction_router",
    "train_router",
    "upload_router",
]
