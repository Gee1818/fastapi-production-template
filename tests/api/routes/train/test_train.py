from pathlib import Path

import polars as pl
from fastapi import status
from fastapi.testclient import TestClient

from app.settings import Settings


def test_train_endpoint_success(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
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
    train_file = Settings.DEFAULT_TRAINING_FILE

    train_file.unlink(missing_ok=True)

    response = client.post("/train/train")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_train_endpoint_creates_model_file(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    model_path = Settings.MODEL_PATH
    model_path.unlink(missing_ok=True)

    response = client.post("/train/train")

    assert response.status_code == status.HTTP_200_OK
    assert model_path.exists()
    assert model_path.stat().st_size > 0


def test_train_endpoint_response_format(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    response = client.post("/train/train")

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
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    response1 = client.post("/train/train")
    model_size_1 = Settings.MODEL_PATH.stat().st_size

    response2 = client.post("/train/train")
    model_size_2 = Settings.MODEL_PATH.stat().st_size

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK

    assert response1.json()["message"] == "Model trained successfully"
    assert response2.json()["message"] == "Model trained successfully"

    assert Settings.MODEL_PATH.exists()
    assert model_size_1 > 0
    assert model_size_2 > 0


def test_train_endpoint_with_minimal_csv(client: TestClient) -> None:

    minimal_df = pl.DataFrame({
        "Event": ["Blitz"] * 5 + ["Rapid"] * 5 + ["Blitz"] * 5,
        "Result": [1, 1, -1, -1, 0] * 3,
        "WhiteElo": [1500, 1600, 1700, 1800, 1900] * 3,
        "BlackElo": [1500, 1600, 1700, 1800, 1900] * 3,
        "ECO": ["A00", "B00", "C00", "D00", "E00"] * 3,
        "Opening": ["Test1", "Test2", "Test3", "Test4", "Test5"] * 3,
        "TimeControl": ["180+0"] * 15,
        "Termination": ["Normal"] * 15,
        "white_material": [38] * 15,
        "black_material": [38] * 15,
        "material_diff": [0] * 15,
        "white_pieces_attacked": [3] * 15,
        "white_attacked_value": [7] * 15,
        "black_pieces_attacked": [4] * 15,
        "black_attacked_value": [8] * 15,
        "attacked_diff": [1] * 15,
        "white_center_pieces": [1] * 15,
        "black_center_pieces": [1] * 15,
        "white_center_control": [3] * 15,
        "black_center_control": [3] * 15,
        "center_control_diff": [0] * 15,
        "white_extended_control": [12] * 15,
        "black_extended_control": [11] * 15,
        "extended_control_diff": [1] * 15,
        "white_mobility": [45] * 15,
        "black_mobility": [42] * 15,
        "mobility_diff": [3] * 15,
        "white_weighted_mobility": [195.0] * 15,
        "black_weighted_mobility": [0.0] * 15,
        "weighted_mobility_diff": [195.0] * 15,
        "position_advantage": [-1] * 15,
        "center_advantage": [1] * 15,
        "aggression": [1] * 15,
        "pawn_structure": [-2] * 15,
        "pieces_protected": [-2] * 15,
        "degrees_of_freedom": [3] * 15,
        "opponent_aggression": [3] * 15,
        "queen_position": [4] * 15,
        "knight_position": [0] * 15,
        "bishop_position": [-1] * 15,
        "rook_position": [2] * 15,
        "pawn_position": [0] * 15,
        "dof_x_material": [3306.0] * 15,
    })

    default_path = Settings.DEFAULT_TRAINING_FILE
    minimal_df.write_csv(default_path)

    response = client.post("/train/train")

    assert response.status_code == status.HTTP_200_OK


def test_train_endpoint_handles_concurrent_requests(
    client: TestClient,
    sample_train_csv_file: Path,
) -> None:
    default_path = Settings.DEFAULT_TRAINING_FILE
    sample_train_csv_file.rename(default_path)

    response1 = client.post("/train/train")
    response2 = client.post("/train/train")

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK

    assert Settings.MODEL_PATH.exists()
