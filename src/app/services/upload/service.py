from fastapi import UploadFile
from pydantic import BaseModel

from app.domain import UploadServiceResponse
from app.services.preprocessing.service import PreprocessingService


class UploadService(BaseModel):
    preprocessing_service: PreprocessingService

    def save_file(self, file: UploadFile) -> UploadServiceResponse:

        result = self.preprocessing_service.process_file(file)

        return UploadServiceResponse(
            message=result.message,
            total_features=result.total_features,
            total_rows=result.total_rows,
        )
