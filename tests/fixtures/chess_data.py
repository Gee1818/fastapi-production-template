import io
from pathlib import Path

import pytest
from fastapi import UploadFile

# Test data directory
TEST_DATA_DIR = Path(__file__).parent.parent / "data"


def _load_pgn_file(filename: str) -> str:
    """Load PGN data from a file in the test data directory.

    Args:
        filename: Name of the PGN file to load

    Returns:
        Content of the PGN file as a string
    """
    file_path = TEST_DATA_DIR / filename
    return file_path.read_text(encoding="utf-8")


@pytest.fixture
def valid_pgn_data() -> str:
    return _load_pgn_file("valid_games.pgn")


@pytest.fixture
def invalid_elo_pgn() -> str:
    return _load_pgn_file("invalid_elo.pgn")


@pytest.fixture
def too_few_moves_pgn() -> str:
    return _load_pgn_file("too_few_moves.pgn")


@pytest.fixture
def wrong_event_type_pgn() -> str:
    return _load_pgn_file("wrong_event_type.pgn")


@pytest.fixture
def valid_upload_file(valid_pgn_data: str) -> UploadFile:
    file_obj = io.BytesIO(valid_pgn_data.encode())
    return UploadFile(filename="valid_test.pgn", file=file_obj)


@pytest.fixture
def invalid_elo_upload_file(invalid_elo_pgn: str) -> UploadFile:
    file_obj = io.BytesIO(invalid_elo_pgn.encode())
    return UploadFile(filename="invalid_elo_test.pgn", file=file_obj)


@pytest.fixture
def too_few_moves_upload_file(too_few_moves_pgn: str) -> UploadFile:
    file_obj = io.BytesIO(too_few_moves_pgn.encode())
    return UploadFile(filename="too_few_moves_test.pgn", file=file_obj)


@pytest.fixture
def wrong_event_upload_file(wrong_event_type_pgn: str) -> UploadFile:
    file_obj = io.BytesIO(wrong_event_type_pgn.encode())
    return UploadFile(filename="wrong_event_test.pgn", file=file_obj)
