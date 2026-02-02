from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import ReadFileServiceDependency

from .schemas import ReadPGNResponse

router = APIRouter(prefix="/read-pgn", tags=["read-pgn"])


@router.post("/read-pgn")
@inject
def read_pgn(
    file: Annotated[UploadFile, File(...)],
    read_file_service: ReadFileServiceDependency,
) -> ReadPGNResponse:
    service_response = read_file_service.read_pgn(file)
    response_data = service_response.model_dump()
    return ReadPGNResponse(**response_data)
