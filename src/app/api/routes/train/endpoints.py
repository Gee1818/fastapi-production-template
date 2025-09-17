from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import TrainingServiceDependency

from .responses import RESPONSES
from .schemas import TrainRequest, TrainResponse

router = APIRouter(prefix="/train", tags=["Train"])


@router.post("/train", responses=RESPONSES)
@inject
async def train(
    file: Annotated[UploadFile, File(...)],
    training_service: TrainingServiceDependency,
) -> TrainResponse:
    features, result = training_service.prepare_data(file)
    req = TrainRequest(features=features, result=result)  # type: ignore[arg-type]

    X_matrix = [[f.whiteElo, f.blackElo] for f in req.features]

    training_service.train(X_matrix, req.result)
    return TrainResponse()
