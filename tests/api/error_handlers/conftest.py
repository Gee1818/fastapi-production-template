import pytest
from fastapi import Request
from starlette.datastructures import Headers


@pytest.fixture
def mock_request() -> Request:
    """Create a mock Request object for testing error handlers.

    Returns:
        Request: A mock Request object.
    """
    return Request(
        scope={
            "type": "http",
            "method": "POST",
            "path": "/test",
            "headers": Headers().raw,
            "query_string": b"",
            "server": ("testserver", 80),
        }
    )
