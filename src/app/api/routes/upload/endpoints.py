from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import UploadServiceDependency

from .schemas import UploadResponse

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/upload")
@inject
def train(
    file: Annotated[UploadFile, File(...)],
    upload_service: UploadServiceDependency,
) -> UploadResponse:
    service_response = upload_service.save_file(file)
    response_data = service_response.model_dump()
    return UploadResponse(**response_data)
