from collections.abc import Callable

from fastapi import Request, Response

from app.services.exceptions import DataValidationError
from app.services.training import DimensionalityMismatchError

from .training import data_validation_error_handler, dimensionality_mismatch_handler

ExceptionHandler = Callable[[Request, Exception], Response]

EXCEPTION_HANDLERS: dict[type[Exception], ExceptionHandler] = {
    DimensionalityMismatchError: dimensionality_mismatch_handler,  # type: ignore[dict-item]
    DataValidationError: data_validation_error_handler,  # type: ignore[dict-item]
}

__all__ = ["EXCEPTION_HANDLERS"]
