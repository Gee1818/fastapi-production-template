import pytest
from fastapi import status
from fastapi.testclient import TestClient
from syrupy.assertion import SnapshotAssertion

from app.settings import Settings


def test_train_endpoint_success(
    client: TestClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that train endpoint works when train.csv exists."""
    # Verify train.csv exists (from your documents, it should)
    train_file = Settings.DEFAULT_TRAINING_FILE

    if not train_file.exists():
        pytest.skip("train.csv not found in uploads directory")

    response = client.post("/train/train")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot


def test_train_endpoint_without_training_file(
    client: TestClient,
) -> None:
    """Test that train endpoint returns 500 when train.csv doesn't exist."""
    # Temporarily rename train.csv if it exists
    train_file = Settings.DEFAULT_TRAINING_FILE
    backup_file = Settings.UPLOAD_DIRECTORY / "train.csv.bak"

    file_existed = train_file.exists()
    if file_existed:
        train_file.rename(backup_file)

    try:
        response = client.post("/train/train")

        # Should return 500 Internal Server Error
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        # Restore train.csv if it existed
        if file_existed:
            if backup_file.exists():
                backup_file.rename(train_file)
            elif not train_file.exists():
                # If somehow the file got lost, skip the test
                pytest.skip("Could not restore train.csv file")


def test_train_endpoint_creates_model(
    client: TestClient,
) -> None:
    """Test that train endpoint creates a model file."""
    train_file = Settings.DEFAULT_TRAINING_FILE

    if not train_file.exists():
        pytest.skip("train.csv not found in uploads directory")

    # Remove model if it exists
    model_path = Settings.MODEL_PATH
    model_path.unlink(missing_ok=True)

    response = client.post("/train/train")

    assert response.status_code == status.HTTP_200_OK

    # Verify model was created
    assert model_path.exists()


def test_train_endpoint_response_format(
    client: TestClient,
) -> None:
    """Test that train endpoint returns correct response format."""
    train_file = Settings.DEFAULT_TRAINING_FILE

    if not train_file.exists():
        pytest.skip("train.csv not found in uploads directory")

    response = client.post("/train/train")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert data["message"] == "Model trained successfully"


def test_train_endpoint_can_train_multiple_times(
    client: TestClient,
) -> None:
    """Test that train endpoint can be called multiple times."""
    train_file = Settings.DEFAULT_TRAINING_FILE

    if not train_file.exists():
        pytest.skip("train.csv not found in uploads directory")

    # First training
    response1 = client.post("/train/train")
    assert response1.status_code == status.HTTP_200_OK

    # Second training (should overwrite model)
    response2 = client.post("/train/train")
    assert response2.status_code == status.HTTP_200_OK

    # Both should succeed
    assert response1.json()["message"] == "Model trained successfully"
    assert response2.json()["message"] == "Model trained successfully"
