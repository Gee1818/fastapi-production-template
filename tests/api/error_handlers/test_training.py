from fastapi import status
from fastapi.testclient import TestClient


def test_data_validation_error_handler(client: TestClient) -> None:
    """Test that data validation error is handled correctly."""
    # Invalid ELO rating (below minimum of 400)
    invalid_elo_data = """result,whiteElo,blackElo
-1,100,1671
1,2262,2191
"""

    response = client.post(
        "/train/train",
        files={"file": ("test.csv", invalid_elo_data.encode(), "text/csv")},
    )

    # The error handler should return 400 status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()
    assert "validation" in response.json()["detail"].lower()
