from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from app.services import (
    PredictionService,
    ReadFileService,
    TrainingService,
    UploadService,
)

PredictionServiceDependency = Annotated[
    PredictionService,
    Depends(Provide["prediction_service"]),
]

TrainingServiceDependency = Annotated[
    TrainingService,
    Depends(Provide["training_service"]),
]

UploadServiceDependency = Annotated[
    UploadService,
    Depends(Provide["upload_service"]),
]

ReadFileServiceDependency = Annotated[
    ReadFileService,
    Depends(Provide["read_file_service"]),
]
