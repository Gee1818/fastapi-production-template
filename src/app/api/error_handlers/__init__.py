from collections.abc import Callable

from fastapi import Request, Response

from app.services.exceptions import DataValidationError

from .training import data_validation_error_handler

ExceptionHandler = Callable[[Request, Exception], Response]

EXCEPTION_HANDLERS: dict[type[Exception], ExceptionHandler] = {
    DataValidationError: data_validation_error_handler,  # type: ignore[dict-item]
}

__all__ = ["EXCEPTION_HANDLERS"]
