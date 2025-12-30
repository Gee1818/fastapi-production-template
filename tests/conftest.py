"""Root test configuration and shared fixtures."""

from collections.abc import Generator
from pathlib import Path

import polars as pl
import pytest
from fastapi.testclient import TestClient

from app.api import create_app
from app.injections import configure_container
from app.injections.test import TestContainer
from app.settings import Settings

# Import all chess data fixtures to make them available to all tests
pytest_plugins = ["tests.fixtures.chess_data"]


@pytest.fixture(autouse=True, scope="session")
def injector_override() -> None:
    """Override dependency injection container for testing."""
    container = configure_container()
    container.override(TestContainer)
    container.wire(packages=["tests"])


@pytest.fixture
def client() -> TestClient:
    """Fixture providing a FastAPI test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def test_train_csv_path() -> Generator[Path, None, None]:
    """Fixture providing a path for test training CSV files."""
    csv_path = Settings.UPLOAD_DIRECTORY / "test_train.csv"
    csv_path.unlink(missing_ok=True)
    yield csv_path
    csv_path.unlink(missing_ok=True)


@pytest.fixture
def test_model_path() -> Generator[Path, None, None]:
    """Fixture providing a path for test model files."""
    model_path = Settings.MODEL_DIRECTORY / "test_model.joblib"
    model_path.unlink(missing_ok=True)
    yield model_path
    model_path.unlink(missing_ok=True)


@pytest.fixture
def sample_train_csv() -> pl.DataFrame:
    """Fixture providing a sample training CSV DataFrame."""
    return pl.DataFrame({
        "Event": ["Blitz"] * 5 + ["Rapid"] * 5 + ["Blitz"] * 5,
        "Result": [1, 1, -1, -1, 0] * 3,
        "WhiteElo": [2045, 1576, 2315, 2100, 1650] * 3,
        "BlackElo": [2126, 1588, 2282, 2050, 1700] * 3,
        "ECO": ["B56", "A00", "E00", "C50", "D20"] * 3,
        "Opening": [
            "Sicilian Defense",
            "Hungarian Opening",
            "Catalan Opening",
            "Italian Game",
            "Queen's Gambit Accepted",
        ]
        * 3,
        "TimeControl": ["300+0", "180+0", "180+0", "300+0", "180+0"] * 3,
        "Termination": ["Normal"] * 15,
        "white_material": [38, 38, 38, 37, 38] * 3,
        "black_material": [38, 37, 38, 38, 38] * 3,
        "material_diff": [0, 1, 0, -1, 0] * 3,
        "white_pieces_attacked": [3, 1, 4, 2, 3] * 3,
        "white_attacked_value": [7, 1, 6, 5, 7] * 3,
        "black_pieces_attacked": [4, 3, 3, 3, 4] * 3,
        "black_attacked_value": [8, 5, 5, 6, 8] * 3,
        "attacked_diff": [1, 4, -1, 2, 1] * 3,
        "white_center_pieces": [1, 0, 1, 1, 0] * 3,
        "black_center_pieces": [1, 1, 2, 1, 1] * 3,
        "white_center_control": [3, 4, 4, 3, 4] * 3,
        "black_center_control": [3, 3, 4, 3, 3] * 3,
        "center_control_diff": [0, 1, 0, 0, 1] * 3,
        "white_extended_control": [12, 14, 10, 11, 13] * 3,
        "black_extended_control": [11, 9, 10, 10, 10] * 3,
        "extended_control_diff": [1, 5, 0, 1, 3] * 3,
        "white_mobility": [45, 46, 40, 43, 45] * 3,
        "black_mobility": [42, 33, 38, 40, 35] * 3,
        "mobility_diff": [3, 13, 2, 3, 10] * 3,
        "white_weighted_mobility": [195.0, 185.0, 142.0, 180.0, 190.0] * 3,
        "black_weighted_mobility": [0.0, 0.0, 0.0, 0.0, 0.0] * 3,
        "weighted_mobility_diff": [195.0, 195.0, 142.0, 180.0, 190.0] * 3,
        "position_advantage": [-1, 6, -4, 2, 5] * 3,
        "center_advantage": [1, 5, 0, 1, 4] * 3,
        "aggression": [1, 2, -1, 1, 2] * 3,
        "pawn_structure": [-2, 0, 0, -1, 0] * 3,
        "pieces_protected": [-2, 0, -1, -1, 0] * 3,
        "degrees_of_freedom": [3, 13, 2, 3, 10] * 3,
        "opponent_aggression": [3, 5, -3, 2, 4] * 3,
        "queen_position": [4, 5, 0, 3, 5] * 3,
        "knight_position": [0, 0, 2, 1, 0] * 3,
        "bishop_position": [-1, 1, -2, 0, 1] * 3,
        "rook_position": [2, 0, -3, 1, 0] * 3,
        "pawn_position": [0, 0, 0, 0, 0] * 3,
        "dof_x_material": [3306.0, 2969.0, 2964.0, 3200.0, 3000.0] * 3,
    })


@pytest.fixture
def sample_train_csv_file(
    sample_train_csv: pl.DataFrame,
    test_train_csv_path: Path,
) -> Path:
    """Fixture providing a sample training CSV file."""
    sample_train_csv.write_csv(test_train_csv_path)
    return test_train_csv_path


@pytest.fixture(autouse=True)
def cleanup_test_files() -> Generator[None, None, None]:
    """Clean up any test files created during testing."""
    yield

    test_files = [
        Settings.UPLOAD_DIRECTORY / "test_train.csv",
        Settings.UPLOAD_DIRECTORY / "train.csv",
        Settings.MODEL_DIRECTORY / "test_model.joblib",
        Settings.MODEL_DIRECTORY / "model.joblib",
    ]

    for file_path in test_files:
        file_path.unlink(missing_ok=True)
