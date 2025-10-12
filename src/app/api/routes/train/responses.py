from typing import Any

from app.services.exceptions import DataValidationError

RESPONSES: dict[int | str, dict[str, Any]] = {
    422: {
        "description": "Data Validation error",
        "model": DataValidationError,
    },
}
