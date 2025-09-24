from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, Body

from app.api.dependencies import PredictionServiceDependency

from .examples import EXAMPLES
from .schemas import PredictionRequest

router = APIRouter(prefix="/prediction", tags=["Prediction"])


@router.post("/predict")
@inject
async def predict(
    prediction_request: Annotated[PredictionRequest, Body(openapi_examples=EXAMPLES)],
    prediction_service: PredictionServiceDependency,
) -> None:
    pass
