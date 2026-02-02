from collections.abc import Iterable

from fastapi import APIRouter

from .health import health_router
from .prediction import PredictionRequest, PredictionResponse, prediction_router
from .read_pgn import ReadPGNResponse, read_pgn_router
from .train import TrainResponse, train_router

ROUTERS: Iterable[APIRouter] = (  # noqa: RUF067
    health_router,
    prediction_router,
    train_router,
    read_pgn_router,
)

__all__ = [
    "ROUTERS",
    "PredictionRequest",
    "PredictionResponse",
    "ReadPGNResponse",
    "TrainResponse",
    "health_router",
    "prediction_router",
    "read_pgn_router",
    "train_router",
]
