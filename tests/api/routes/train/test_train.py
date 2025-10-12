import io

from fastapi import status
from fastapi.testclient import TestClient
from syrupy.assertion import SnapshotAssertion

dummy_data = """result,whiteElo,blackElo
-1,1706,1671
1,2262,2191
-1,2279,2339
0,971,1040
"""


def test_train_endpoint_success(
    client: TestClient, snapshot: SnapshotAssertion
) -> None:
    response = client.post(
        "/train/train",
        files={"file": ("test.csv", io.BytesIO(dummy_data.encode()), "text/csv")},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot
