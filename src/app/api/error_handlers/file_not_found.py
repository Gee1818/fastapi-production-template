from fastapi import Request
from fastapi.responses import JSONResponse


def file_not_found_error_handler(
    _: Request,
    exc: FileNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
