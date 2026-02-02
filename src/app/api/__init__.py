import uvicorn

from app.settings import Settings

from .app import create_app


def run_api() -> None:  # noqa: RUF067
    uvicorn.run(
        "app.api:create_app",
        factory=True,
        host=Settings.HOST,
        port=Settings.API_PORT,
    )


__all__ = ["create_app", "run_api"]
