import io

from fastapi import status
from fastapi.testclient import TestClient
from syrupy.assertion import SnapshotAssertion

# Valid PGN format data with multiple games
dummy_data = """[Event "Rated Blitz game"]
[Site "https://lichess.org/test1"]
[Date "2025.07.01"]
[Round "-"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1706"]
[BlackElo "1671"]
[WhiteRatingDiff "+6"]
[BlackRatingDiff "-6"]
[ECO "A43"]
[Opening "Test Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Na5 10. Bc2 c5 11. d4 Qc7 12. Nbd2 cxd4 13. cxd4 Nc6 14. Nb3 a5 15. Be3 a4 16. Nbd2 Bd7 1-0

[Event "Rated Blitz game"]
[Site "https://lichess.org/test2"]
[Date "2025.07.01"]
[Round "-"]
[White "Player3"]
[Black "Player4"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "2262"]
[BlackElo "2191"]
[WhiteRatingDiff "-5"]
[BlackRatingDiff "+5"]
[ECO "A46"]
[Opening "Test Opening 2"]
[TimeControl "180+0"]
[Termination "Normal"]

1. d4 d5 2. c4 dxc4 3. Nf3 Nf6 4. e3 e6 5. Bxc4 c5 6. O-O a6 7. dxc5 Qxd1 8. Rxd1 Bxc5 9. Nbd2 O-O 10. Nb3 Be7 11. Bd2 Nc6 12. Rac1 Bd7 13. Be2 Rfd8 14. Bc3 Be8 15. Nbd4 Nxd4 16. Nxd4 Nd7 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/test3"]
[Date "2025.07.01"]
[Round "-"]
[White "Player5"]
[Black "Player6"]
[Result "1/2-1/2"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1800"]
[BlackElo "1750"]
[WhiteRatingDiff "0"]
[BlackRatingDiff "0"]
[ECO "C50"]
[Opening "Test Opening 3"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. O-O Nf6 5. d3 d6 6. c3 O-O 7. Bb3 a6 8. Nbd2 Ba7 9. h3 h6 10. Re1 Re8 11. Nf1 Be6 12. Ng3 Bxb3 13. axb3 d5 14. Qe2 dxe4 15. dxe4 Qxd1 16. Rxd1 Rad8 1/2-1/2

[Event "Rated Blitz game"]
[Site "https://lichess.org/test4"]
[Date "2025.07.01"]
[Round "-"]
[White "Player7"]
[Black "Player8"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1900"]
[BlackElo "1850"]
[WhiteRatingDiff "+5"]
[BlackRatingDiff "-5"]
[ECO "D00"]
[Opening "Test Opening 4"]
[TimeControl "180+0"]
[Termination "Normal"]

1. d4 d5 2. Bf4 Nf6 3. e3 e6 4. Nd2 Bd6 5. Bg3 O-O 6. Ngf3 c5 7. c3 Nc6 8. Bd3 b6 9. Ne5 Bb7 10. Qf3 Qc7 11. h4 h6 12. Nxc6 Bxc6 13. Bxd6 Qxd6 14. dxc5 bxc5 15. O-O Rab8 16. b3 a5 1-0

[Event "Rated Blitz game"]
[Site "https://lichess.org/test5"]
[Date "2025.07.01"]
[Round "-"]
[White "Player9"]
[Black "Player10"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1650"]
[BlackElo "1680"]
[WhiteRatingDiff "-5"]
[BlackRatingDiff "+5"]
[ECO "B10"]
[Opening "Test Opening 5"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 c6 2. Nf3 d5 3. exd5 cxd5 4. d4 Nc6 5. Bf4 Nf6 6. c3 Bg4 7. Nbd2 e6 8. Be2 Bd6 9. Bxd6 Qxd6 10. O-O O-O 11. h3 Bh5 12. Re1 Rae8 13. Nf1 Bg6 14. Ng3 Ne4 15. Nxe4 Bxe4 16. Nd2 Bg6 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/test6"]
[Date "2025.07.01"]
[Round "-"]
[White "Player11"]
[Black "Player12"]
[Result "1/2-1/2"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1700"]
[BlackElo "1710"]
[WhiteRatingDiff "0"]
[BlackRatingDiff "0"]
[ECO "C41"]
[Opening "Test Opening 6"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 d6 3. d4 exd4 4. Nxd4 Nf6 5. Nc3 Be7 6. Be2 O-O 7. O-O c6 8. f4 Nbd7 9. Bf3 Nc5 10. Qe2 Bg4 11. Bxg4 Nxg4 12. h3 Nf6 13. Be3 Nfd7 14. Rad1 Bf6 15. Nf3 Re8 16. Qf2 Qc7 1/2-1/2

[Event "Rated Blitz game"]
[Site "https://lichess.org/test7"]
[Date "2025.07.01"]
[Round "-"]
[White "Player13"]
[Black "Player14"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "2000"]
[BlackElo "1950"]
[WhiteRatingDiff "+5"]
[BlackRatingDiff "-5"]
[ECO "A00"]
[Opening "Test Opening 7"]
[TimeControl "180+0"]
[Termination "Normal"]

1. g3 d5 2. Bg2 e5 3. d3 Nf6 4. Nf3 Nc6 5. O-O Be7 6. Nbd2 O-O 7. e4 d4 8. Nc4 Bg4 9. h3 Bh5 10. g4 Bg6 11. Nh4 Nd7 12. Nxg6 hxg6 13. f4 exf4 14. Bxf4 Nc5 15. Qd2 Ne6 16. Be5 Nxe5 1-0

[Event "Rated Blitz game"]
[Site "https://lichess.org/test8"]
[Date "2025.07.01"]
[Round "-"]
[White "Player15"]
[Black "Player16"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1500"]
[BlackElo "1550"]
[WhiteRatingDiff "-4"]
[BlackRatingDiff "+4"]
[ECO "C45"]
[Opening "Test Opening 8"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. d4 exd4 4. Nxd4 Nf6 5. Nxc6 bxc6 6. Bd3 d5 7. exd5 cxd5 8. O-O Be7 9. Nc3 O-O 10. Bg5 c6 11. Qf3 Be6 12. Rfe1 h6 13. Bh4 Rb8 14. Rab1 Qd7 15. Na4 Bd6 16. Nc5 Bxc5 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/test9"]
[Date "2025.07.01"]
[Round "-"]
[White "Player17"]
[Black "Player18"]
[Result "1/2-1/2"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1820"]
[BlackElo "1810"]
[WhiteRatingDiff "0"]
[BlackRatingDiff "0"]
[ECO "B20"]
[Opening "Test Opening 9"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 c5 2. Bc4 e6 3. Nc3 a6 4. a4 Nc6 5. Nf3 Nf6 6. d3 Be7 7. O-O O-O 8. Be3 d6 9. Qe2 b6 10. Rfd1 Bb7 11. Bf1 Qc7 12. h3 Rfd8 13. Rac1 Rac8 14. Qf1 Nd7 15. Ne2 Bf6 16. c3 Be7 1/2-1/2

[Event "Rated Blitz game"]
[Site "https://lichess.org/test10"]
[Date "2025.07.01"]
[Round "-"]
[White "Player19"]
[Black "Player20"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1750"]
[BlackElo "1720"]
[WhiteRatingDiff "+5"]
[BlackRatingDiff "-5"]
[ECO "D20"]
[Opening "Test Opening 10"]
[TimeControl "180+0"]
[Termination "Normal"]

1. d4 d5 2. c4 dxc4 3. e4 Nf6 4. e5 Nd5 5. Bxc4 Nb6 6. Bd3 Nc6 7. Nf3 Bg4 8. O-O e6 9. Nc3 Be7 10. h3 Bh5 11. Be3 O-O 12. Qe2 Nd5 13. Nxd5 exd5 14. Rac1 Bg6 15. Bxg6 hxg6 16. Qd3 Qd7 1-0
"""


def test_train_endpoint_success(
    client: TestClient, snapshot: SnapshotAssertion
) -> None:
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
