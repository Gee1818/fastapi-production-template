import io
from typing import Annotated

import polars as pl
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
    contents = await file.read()
    df = pl.read_csv(io.BytesIO(contents))
    X = df.select(["whiteElo", "blackElo"]).to_dicts()
    y = df["result"].to_list()

    req = TrainRequest(features=X, result=y)  # pyright: ignore[reportArgumentType]

    X_matrix = [[f.whiteElo, f.blackElo] for f in req.features]

    training_service.train(X_matrix, req.result)
    return TrainResponse()
