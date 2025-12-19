from dependency_injector.wiring import inject
from fastapi import APIRouter

from app.api.dependencies import TrainingServiceDependency
from app.settings import Settings

from .responses import RESPONSES
from .schemas import TrainResponse

router = APIRouter(prefix="/train", tags=["train"])


@router.post("/train", responses=RESPONSES)
@inject
def train(
    training_service: TrainingServiceDependency,
) -> TrainResponse:
    training_service.train(Settings.DEFAULT_TRAINING_FILE)
    return TrainResponse()
