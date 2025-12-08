from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import PredictionServiceDependency

from .schemas import PredictionResponse

router = APIRouter(prefix="/prediction", tags=["Prediction"])


@router.post("/predict")
@inject
async def predict(
    prediction_request: Annotated[UploadFile, File(...)],
    prediction_service: PredictionServiceDependency,
) -> PredictionResponse:
    prediction_service.predict(prediction_request)
    return PredictionResponse()
