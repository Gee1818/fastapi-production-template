import io

from fastapi import status
from fastapi.testclient import TestClient
from syrupy.assertion import SnapshotAssertion

dummy_data = """
[Event "Rated Blitz game"]
[Site "https://lichess.org/VsUqVhC2"]
[Date "2025.07.01"]
[Round "-"]
[White "my_name_jeff"]
[Black "xxxgrishaxxx"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1706"]
[BlackElo "1671"]
[WhiteRatingDiff "-6"]
[BlackRatingDiff "+6"]
[ECO "A43"]
[Opening "Benoni Defense: Old Benoni"]
[TimeControl "180+0"]
[Termination "Normal"]

1. d4 c5 2. e3 e6 3. dxc5 Bxc5 4. Nf3 Nf6 5. c3 Nc6 6. Bb5 a6 7. Bxc6 bxc6 8. O-O d5 9. Nd4 Bd7 10. Qf3 O-O 11. h4 e5 12. Nc2 Bd6 13. h5 e4 14. Qe2 Bg4 15. f3 exf3 16. gxf3 Bxh5 17. e4 dxe4 18. Ne1 exf3 19. Nxf3 Qd7 20. Bg5 Qg4+ 21. Qg2 Qxg2+ 22. Kxg2 Bxf3+ 23. Rxf3 Ne4 24. Be3 h6 25. Nd2 Rfe8 26. Nxe4 Rxe4 27. Bd4 Rae8 28. Raf1 c5 29. Bg1 f6 30. a3 Re2+ 31. Bf2 Rxb2 32. Kh3 Ree2 33. Kg2 c4 34. a4 Bc5 35. Re3 Bxe3 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/dAPM8wzS"]
[Date "2025.07.01"]
[Round "-"]
[White "Lostratega"]
[Black "abdo0diab2000"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "2262"]
[BlackElo "2191"]
[WhiteRatingDiff "+5"]
[BlackRatingDiff "-5"]
[ECO "A46"]
[Opening "Indian Defense: Wade-Tartakower Defense"]
[TimeControl "180+0"]
[Termination "Normal"]

1. d4 d6 2. Nf3 Nf6 3. c4 d5 4. Nc3 Bg4 5. cxd5 Bxf3 6. exf3 Nxd5 7. Bc4 c6 8. Qb3 Nxc3 9. bxc3 Qb6 10. Bxf7+ Kd8 11. Qe6 Nd7 12. O-O Nf6 13. Bg5 Nd5 14. c4 Nc7 15. Qe4 Qa5 16. Bf4 Kd7 17. Bxc7 Kxc7 18. d5 Rd8 19. dxc6 bxc6 20. Rab1 e5 21. c5 Qxc5 22. Rfc1 Qd6 23. h3 Be7 24. Bb3 Qd4 25. Qxc6+ Kb8 26. Bd5+ Bb4 27. Qb7# 1-0

[Event "Rated Blitz game"]
[Site "https://lichess.org/aoCEGX3k"]
[Date "2025.07.01"]
[Round "-"]
[White "YarnHugen"]
[Black "LateralusMind"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "2279"]
[BlackElo "2339"]
[WhiteRatingDiff "-5"]
[BlackRatingDiff "+4"]
[ECO "A46"]
[Opening "Yusupov-Rubinstein System"]
[TimeControl "180+0"]
[Termination "Normal"]

1. d4 Nf6 2. Nf3 e6 3. e3 Be7 4. Bd3 b6 5. O-O Bb7 6. b3 c5 7. Bb2 cxd4 8. e4 O-O 9. Re1 d6 10. Nxd4 Nbd7 11. Nd2 a6 12. a3 Rc8 13. N2f3 Rc7 14. Qd2 Qa8 15. Rad1 Nxe4 16. Bxe4 Bxe4 17. c4 Nf6 18. h3 Rd8 19. Qe3 Bb7 20. Ng5 e5 21. Nde6 fxe6 22. Nxe6 Rcd7 23. Nxd8 Qxd8 24. b4 Qa8 25. g3 Bf3 26. Rd3 Bh1 27. f3 e4 28. fxe4 Bxe4 29. Rd2 Bg6 30. Qe6+ Bf7 31. Bxf6 Bxe6 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/yNTMyTZV"]
[Date "2025.07.01"]
[Round "-"]
[White "Timon_01"]
[Black "tbruins82"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1471"]
[BlackElo "1540"]
[WhiteRatingDiff "-16"]
[BlackRatingDiff "+4"]
[ECO "A00"]
[Opening "Polish Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. b4 e5 2. Bb2 f5 3. Bxe5 Bc5 4. Bxg7 Bxf2+ 5. Kxf2 Qg5 6. Bxh8 Nf6 7. Bxf6 Qxf6 8. Ke1 Qxa1 9. Nc3 Qxa2 10. Qb1 Qe6 11. Nf3 Qh6 12. e3 d6 13. Bc4 Nc6 14. Kf2 Be6 15. Bxe6 Qxe6 16. Ng5 Qh6 17. Nf3 O-O-O 18. Qb3 Ne5 19. Nxe5 dxe5 20. h3 Rxd2+ 21. Kg1 Qh4 22. Kh2 f4 23. Ne4 fxe3 24. Nxd2 Qf4+ 25. g3 Qf2# 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/8BMCO7Nj"]
[Date "2025.07.01"]
[Round "-"]
[White "birddead"]
[Black "jay623"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1752"]
[BlackElo "1737"]
[WhiteRatingDiff "-6"]
[BlackRatingDiff "+6"]
[ECO "C41"]
[Opening "Philidor Defense"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 d6 3. Bc4 Be7 4. d4 h6 5. dxe5 a6 6. exd6 cxd6 7. Nc3 Nc6 8. O-O Na5 9. Bd5 Nc6 10. h3 Bd7 11. Bf4 Nf6 12. Bb3 Na5 13. Nd5 Nxd5 14. Bxd5 Bc6 15. Bxc6+ bxc6 16. Qd2 O-O 17. Rad1 d5 18. exd5 cxd5 19. Qxd5 Bf6 20. Qxd8 Rfxd8 21. Be5 Rxd1 22. Rxd1 Bxe5 23. Nxe5 Re8 24. Nf3 Nc4 25. b3 Na3 26. c4 a5 27. c5 a4 28. bxa4 Nc4 29. c6 Rc8 30. Nd4 Ne5 31. Rc1 g6 32. a5 f5 33. a6 Kf7 34. a7 Ra8 35. c7 Rxa7 36. c8=Q Rxa2 37. Rc7+ Kf6 38. Qe6+ Kg5 39. h4+ Kf4 40. Qxe5+ Kxe5 41. Re7+ Kxd4 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/oZg3qWYl"]
[Date "2025.07.01"]
[Round "-"]
[White "a_Random_Rook"]
[Black "Tomorrow_Man"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1786"]
[BlackElo "1801"]
[WhiteRatingDiff "-5"]
[BlackRatingDiff "+6"]
[ECO "B00"]
[Opening "Owen Defense"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 b6 2. d3 Bb7 3. Nc3 g6 4. Be3 Bg7 5. Nf3 e6 6. Be2 Ne7 7. Qd2 d5 8. O-O-O d4 9. Bxd4 Bxd4 10. Nxd4 Qxd4 11. f4 Nbc6 12. g4 O-O-O 13. f5 gxf5 14. gxf5 exf5 15. exf5 Nxf5 16. Qg5 Qe3+ 17. Qxe3 Nxe3 18. Rdg1 Rhg8 19. Re1 Nd4 20. Bh5 Bxh1 21. Rxe3 Bb7 22. h3 Rg1+ 23. Kd2 Rdg8 24. Bg4+ Kb8 25. Re7 Bc8 26. Nd5 Bxg4 27. hxg4 Rg2+ 28. Kc3 Nb5+ 29. Kb4 Nd6 30. Nxc7 R2xg4+ 31. Kc3 R8g5 32. Ne8 Nb5+ 33. Kb3 Rg2 34. Rxf7 Nd4+ 35. Kc3 Ne2+ 36. Kb3 Rb5+ 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/yUEcdPCa"]
[Date "2025.07.01"]
[Round "-"]
[White "ale_998"]
[Black "ArtyCranner"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1444"]
[BlackElo "1425"]
[WhiteRatingDiff "-6"]
[BlackRatingDiff "+7"]
[ECO "A00"]
[Opening "Van't Kruijs Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e3 c6 2. d4 d5 3. c4 Bf5 4. Nc3 e6 5. Bd3 Bxd3 6. Qxd3 Nf6 7. cxd5 cxd5 8. Nf3 Nc6 9. O-O Qb6 10. Ne5 Nxe5 11. dxe5 Nd7 12. b3 Nxe5 13. Qc2 Bd6 14. Na4 Qc7 15. Bb2 Qxc2 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/MIxT6upK"]
[Date "2025.07.01"]
[Round "-"]
[White "likerszap"]
[Black "vincgrandmaster"]
[Result "0-1"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1950"]
[BlackElo "1946"]
[WhiteRatingDiff "-6"]
[BlackRatingDiff "+6"]
[ECO "A00"]
[Opening "Hungarian Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. g3 e5 2. Bg2 Nf6 3. e4 c6 4. c4 d5 5. cxd5 cxd5 6. exd5 Nxd5 7. Ne2 Be6 8. O-O Nc6 9. d4 e4 10. a3 Bf5 11. b4 Bd6 12. Qb3 Nb6 13. d5 Nd4 14. Nxd4 Be5 15. Bb2 Qf6 16. Rd1 O-O 17. Nd2 Qh6 18. Nxf5 Qg5 19. Ne3 Rae8 20. Bxe5 Qxe5 21. d6 Rd8 22. Ndc4 Nxc4 23. Nxc4 Qf5 24. Re1 Qf6 25. Bxe4 Qe6 26. Bxb7 Qf6 27. Ba6 Qg6 28. Rad1 Qf6 29. Ne5 Qf6 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/PQKFGjSt"]
[Date "2025.07.01"]
[Round "-"]
[White "br0ze-YT"]
[Black "QueenPalestine"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:31"]
[WhiteElo "1579"]
[BlackElo "1511"]
[WhiteRatingDiff "+5"]
[BlackRatingDiff "-4"]
[ECO "A05"]
[Opening "Zukertort Opening: Lemberger Gambit"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 Nf6 2. Nf3 d6 3. d3 c6 4. Nc3 e5 5. Bg5 Be7 6. Be2 O-O 7. Qd2 Qc7 8. O-O-O Rd8 9. h4 h6 10. Ne1 hxg5 11. hxg5 Nh7 12. Qe3 Bxg5 13. f4 Bxf4 14. Qxf4 exf4 15. Nf3 f5 16. Rh4 fxe4 17. dxe4 g5 18. Rh5 Bg4 19. Rh6 Bxf3 20. Bxf3 Nd7 21. Rdh1 Ndf6 22. Rg6+ Kf7 23. Rgh6 Rh8 24. e5 dxe5 25. Ne4 Nxe4 26. Bxe4 Kg8 27. Bxh7+ Rxh7 28. Rg6+ Kh8 29. Rd1 Rg8 30. Rgd6 g4 31. R6d2 f3 32. gxf3 gxf3 33. Rf2 Rf8 34. Rdf1 e4 35. a3 Qf4+ 36. Kb1 1-0

"""  # noqa: E501


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
