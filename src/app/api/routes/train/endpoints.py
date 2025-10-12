from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import TrainingServiceDependency

from .responses import RESPONSES
from .schemas import TrainResponse

router = APIRouter(prefix="/train", tags=["train"])


@router.post("/train", responses=RESPONSES)
@inject
def train(
    file: Annotated[UploadFile, File(...)],
    training_service: TrainingServiceDependency,
) -> TrainResponse:
    training_service.train(file)
    return TrainResponse()
