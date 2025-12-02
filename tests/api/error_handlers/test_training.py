from fastapi import status
from fastapi.testclient import TestClient


def test_data_validation_error_handler(client: TestClient) -> None:
    """Test that data validation error is handled correctly."""
    # Invalid ELO rating (below minimum of 400) in PGN format
    invalid_elo_pgn = """[Event "Rated Blitz game"]
[Site "https://lichess.org/test"]
[Date "2025.07.01"]
[Round "-"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "100"]
[BlackElo "1671"]
[WhiteRatingDiff "+6"]
[BlackRatingDiff "-6"]
[ECO "A43"]
[Opening "Test Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Na5 10. Bc2 c5 11. d4 Qc7 12. Nbd2 cxd4 13. cxd4 Nc6 14. Nb3 a5 15. Be3 a4 1-0
"""  # noqa: E501

    response = client.post(
        "/train/train",
        files={
            "file": ("test.pgn", invalid_elo_pgn.encode(), "application/x-chess-pgn")
        },
    )

    # The error handler should return 400 status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()
    assert "validation" in response.json()["detail"].lower()
