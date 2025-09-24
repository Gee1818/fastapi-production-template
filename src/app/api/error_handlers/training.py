from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.exceptions import DataValidationError
from app.services.training import DimensionalityMismatchError


def dimensionality_mismatch_handler(
    _: Request,
    exc: DimensionalityMismatchError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


def data_validation_error_handler(
    _: Request,
    exc: DataValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
