from fastapi import status
from fastapi.testclient import TestClient
from syrupy.assertion import SnapshotAssertion

dummy_data = """
result,white_elo,black_elo
-1,1706,1671
1,2262,2191
-1,2279,2339
0,971,1040
"""


def test_train_endpoint(client: TestClient, snapshot: SnapshotAssertion) -> None:
    response = client.post("/train/train", json={"data": dummy_data})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot
