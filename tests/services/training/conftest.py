from collections.abc import Generator
from pathlib import Path

import pytest
from dependency_injector.wiring import Provide, inject

from app.services.training import TrainingService
from app.settings import Settings


@pytest.fixture
def model_path() -> Generator[Path]:
    model_path = Settings.MODEL_DIRECTORY / "model_test.joblib"
    model_path.unlink(missing_ok=True)
    yield model_path
    model_path.unlink(missing_ok=True)


@pytest.fixture
@inject
def training_service(
    model_path: Path,
    training_service_: TrainingService = Provide["training_service"],
) -> TrainingService:
    training_service_.model_path = model_path
    return training_service_


@pytest.fixture
def training_data_dimension_mismatch() -> tuple[list[list[float]], list[float]]:
    X = [[25.0], [30.0], [35.0]]
    y = [5.0, 6.0]
    return X, y


@pytest.fixture
def valid_chess_data() -> str:
    return """[Event "Rated Blitz game"]
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
"""  # noqa: E501


@pytest.fixture
def invalid_elo_data() -> str:
    return """[Event "Rated Blitz game"]
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


@pytest.fixture
def invalid_result_data() -> str:
    return """[Event "Rated Blitz game"]
[Site "https://lichess.org/test"]
[Date "2025.07.01"]
[Round "-"]
[White "Player1"]
[Black "Player2"]
[Result "2-0"]
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

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Na5 10. Bc2 c5 11. d4 Qc7 12. Nbd2 cxd4 13. cxd4 Nc6 14. Nb3 a5 15. Be3 a4 2-0
"""  # noqa: E501
