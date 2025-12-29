"""Tests for /train/train endpoint - Function-based."""

from pathlib import Path

import polars as pl
from fastapi import status
from fastapi.testclient import TestClient

from app.settings import Settings


def test_train_endpoint_success(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    """Test successful model training via endpoint."""
    # Arrange
    # Move the sample file to the default location
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    # Clean up model if exists
    Settings.MODEL_PATH.unlink(missing_ok=True)

    # Act
    response = client.post("/train/train")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert data["message"] == "Model trained successfully"


def test_train_endpoint_without_training_file_fails(client: TestClient) -> None:
    """Test that endpoint fails when train.csv doesn't exist."""
    # Arrange
    train_file = Settings.DEFAULT_TRAINING_FILE
    backup_file = Settings.UPLOAD_DIRECTORY / "train_backup.csv"

    # Backup and remove train.csv if it exists
    file_existed = train_file.exists()
    if file_existed:
        train_file.rename(backup_file)

    try:
        # Act
        response = client.post("/train/train")

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        # Restore train.csv if it existed
        if file_existed and backup_file.exists():
            backup_file.rename(train_file)


def test_train_endpoint_creates_model_file(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    """Test that endpoint creates model file."""
    # Arrange
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    model_path = Settings.MODEL_PATH
    model_path.unlink(missing_ok=True)

    # Act
    response = client.post("/train/train")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert model_path.exists()
    assert model_path.stat().st_size > 0


def test_train_endpoint_response_format(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    """Test that endpoint returns correct response format."""
    # Arrange
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    # Act
    response = client.post("/train/train")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_train_endpoint_can_train_multiple_times(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    """Test that endpoint can be called multiple times successfully."""
    # Arrange
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    # Act - First training
    response1 = client.post("/train/train")
    model_size_1 = Settings.MODEL_PATH.stat().st_size

    # Act - Second training
    response2 = client.post("/train/train")
    model_size_2 = Settings.MODEL_PATH.stat().st_size

    # Assert
    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK

    assert response1.json()["message"] == "Model trained successfully"
    assert response2.json()["message"] == "Model trained successfully"

    # Model should exist and have reasonable size
    assert Settings.MODEL_PATH.exists()
    assert model_size_1 > 0
    assert model_size_2 > 0


def test_train_endpoint_with_minimal_csv(
    client: TestClient,
    test_train_csv_path: Path,
) -> None:
    """Test training with minimal valid CSV."""

    # Arrange - Create minimal valid CSV
    minimal_df = pl.DataFrame({
        "Event": ["Blitz", "Blitz"],
        "Result": [1, -1],
        "WhiteElo": [1500, 1600],
        "BlackElo": [1500, 1600],
        "ECO": ["A00", "A00"],
        "Opening": ["Test", "Test"],
        "TimeControl": ["180+0", "180+0"],
        "Termination": ["Normal", "Normal"],
        "white_material": [38, 38],
        "black_material": [38, 38],
        "material_diff": [0, 0],
        "white_pieces_attacked": [3, 3],
        "white_attacked_value": [7, 7],
        "black_pieces_attacked": [4, 4],
        "black_attacked_value": [8, 8],
        "attacked_diff": [1, 1],
        "white_center_pieces": [1, 1],
        "black_center_pieces": [1, 1],
        "white_center_control": [3, 3],
        "black_center_control": [3, 3],
        "center_control_diff": [0, 0],
        "white_extended_control": [12, 12],
        "black_extended_control": [11, 11],
        "extended_control_diff": [1, 1],
        "white_mobility": [45, 45],
        "black_mobility": [42, 42],
        "mobility_diff": [3, 3],
        "white_weighted_mobility": [195.0, 195.0],
        "black_weighted_mobility": [0.0, 0.0],
        "weighted_mobility_diff": [195.0, 195.0],
        "position_advantage": [-1, -1],
        "center_advantage": [1, 1],
        "aggression": [1, 1],
        "pawn_structure": [-2, -2],
        "pieces_protected": [-2, -2],
        "degrees_of_freedom": [3, 3],
        "opponent_aggression": [3, 3],
        "queen_position": [4, 4],
        "knight_position": [0, 0],
        "bishop_position": [-1, -1],
        "rook_position": [2, 2],
        "pawn_position": [0, 0],
        "dof_x_material": [3306.0, 3306.0],
    })

    default_path = Settings.DEFAULT_TRAINING_FILE
    minimal_df.write_csv(default_path)

    # Act
    response = client.post("/train/train")

    # Assert
    assert response.status_code == status.HTTP_200_OK


def test_train_endpoint_handles_concurrent_requests(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    """Test that endpoint handles concurrent training requests."""
    # Arrange
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    # Act - Simulate concurrent requests (sequential in test)
    response1 = client.post("/train/train")
    response2 = client.post("/train/train")

    # Assert - Both should succeed
    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK

    # Model should be valid
    assert Settings.MODEL_PATH.exists()
