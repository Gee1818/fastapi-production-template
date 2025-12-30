from fastapi import Request
from fastapi.responses import JSONResponse


def file_not_found_error_handler(
    _: Request,
    exc: FileNotFoundError,
) -> JSONResponse:
    """Handle FileNotFoundError by returning a 500 Internal Server Error response.

    Args:
        _: The FastAPI request object (unused)
        exc: The FileNotFoundError exception

    Returns:
        JSONResponse with status code 500 and error details
    """
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
