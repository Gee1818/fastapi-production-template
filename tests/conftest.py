"""Global test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.api import create_app
from app.injections import configure_container
from app.injections.test import TestContainer


@pytest.fixture(autouse=True, scope="session")
def injector_override() -> None:
    """Override dependency injection container for testing."""
    container = configure_container()
    container.override(TestContainer)
    container.wire(packages=["tests"])


@pytest.fixture
def client() -> TestClient:
    """Create FastAPI test client."""
    app = create_app()
    return TestClient(app)
