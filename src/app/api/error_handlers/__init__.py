from collections.abc import Callable

from fastapi import Request, Response

from app.services.exceptions import DataValidationError

from .file_not_found import file_not_found_error_handler
from .training import data_validation_error_handler

ExceptionHandler = Callable[[Request, Exception], Response]  # noqa: RUF067

EXCEPTION_HANDLERS: dict[type[Exception], ExceptionHandler] = {  # noqa: RUF067
    DataValidationError: data_validation_error_handler,  # type: ignore[dict-item]
    FileNotFoundError: file_not_found_error_handler,  # type: ignore[dict-item]
}

__all__ = ["EXCEPTION_HANDLERS"]
