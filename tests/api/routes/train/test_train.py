import io

from fastapi import status
from fastapi.testclient import TestClient
from syrupy.assertion import SnapshotAssertion

from tests.fixtures.chess_data import get_valid_chess_data


def test_train_endpoint_success(
    client: TestClient, snapshot: SnapshotAssertion
) -> None:
    dummy_data = get_valid_chess_data()

    response = client.post(
        "/train/train",
        files={
            "file": (
                "test.pgn",
                io.BytesIO(dummy_data.encode()),
                "application/x-chess-pgn",
            )
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot
