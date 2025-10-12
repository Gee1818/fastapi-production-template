from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.exceptions import DataValidationError


def data_validation_error_handler(
    _: Request,
    exc: DataValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
