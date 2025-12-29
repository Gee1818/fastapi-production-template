"""Shared test fixtures and data generators for chess game testing."""

import io
from collections.abc import Generator
from pathlib import Path

import polars as pl
import pytest
from fastapi import UploadFile

from app.settings import Settings

# Valid PGN data with games that pass all filters
VALID_PGN_DATA = """[Event "Rated Blitz game"]
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

[Event "Rated Rapid game"]
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
[TimeControl "600+0"]
[Termination "Normal"]

1. d4 Nf6 2. Nf3 e6 3. e3 Be7 4. Bd3 b6 5. O-O Bb7 6. b3 c5 7. Bb2 cxd4 8. e4 O-O 9. Re1 d6 10. Nxd4 Nbd7 11. Nd2 a6 12. a3 Rc8 13. N2f3 Rc7 14. Qd2 Qa8 15. Rad1 Nxe4 16. Bxe4 Bxe4 17. c4 Nf6 18. h3 Rd8 19. Qe3 Bb7 20. Ng5 e5 21. Nde6 fxe6 22. Nxe6 Rcd7 23. Nxd8 Qxd8 24. b4 Qa8 25. g3 Bf3 26. Rd3 Bh1 27. f3 e4 28. fxe4 Bxe4 29. Rd2 Bg6 30. Qe6+ Bf7 31. Bxf6 Bxe6 0-1
"""

# Invalid ELO data - ratings outside allowed range
INVALID_ELO_PGN = """[Event "Rated Blitz game"]
[Site "https://lichess.org/test1"]
[Date "2025.07.01"]
[Round "-"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "100"]
[BlackElo "5000"]
[WhiteRatingDiff "+6"]
[BlackRatingDiff "-6"]
[ECO "A00"]
[Opening "Test Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Na5 10. Bc2 c5 11. d4 Qc7 12. Nbd2 cxd4 13. cxd4 Nc6 14. Nb3 a5 15. Be3 a4 1-0
"""

# Too few moves - should be filtered out
TOO_FEW_MOVES_PGN = """[Event "Rated Blitz game"]
[Site "https://lichess.org/test2"]
[Date "2025.07.01"]
[Round "-"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1500"]
[BlackElo "1500"]
[WhiteRatingDiff "+6"]
[BlackRatingDiff "-6"]
[ECO "A00"]
[Opening "Test Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
"""

# Wrong event type - should be filtered out
WRONG_EVENT_TYPE_PGN = """[Event "Casual Blitz game"]
[Site "https://lichess.org/test3"]
[Date "2025.07.01"]
[Round "-"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[UTCDate "2025.07.01"]
[UTCTime "00:00:00"]
[WhiteElo "1500"]
[BlackElo "1500"]
[WhiteRatingDiff "+6"]
[BlackRatingDiff "-6"]
[ECO "A00"]
[Opening "Test Opening"]
[TimeControl "180+0"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Na5 10. Bc2 c5 11. d4 Qc7 12. Nbd2 cxd4 13. cxd4 Nc6 14. Nb3 a5 15. Be3 a4 1-0
"""


@pytest.fixture
def valid_pgn_data() -> str:
    """Return valid PGN data for testing."""
    return VALID_PGN_DATA


@pytest.fixture
def invalid_elo_pgn() -> str:
    """Return PGN data with invalid ELO ratings."""
    return INVALID_ELO_PGN


@pytest.fixture
def too_few_moves_pgn() -> str:
    """Return PGN data with too few moves."""
    return TOO_FEW_MOVES_PGN


@pytest.fixture
def wrong_event_type_pgn() -> str:
    """Return PGN data with wrong event type."""
    return WRONG_EVENT_TYPE_PGN


@pytest.fixture
def valid_upload_file(valid_pgn_data: str) -> UploadFile:
    """Create a valid UploadFile for testing."""
    file_obj = io.BytesIO(valid_pgn_data.encode())
    return UploadFile(filename="valid_test.pgn", file=file_obj)


@pytest.fixture
def invalid_elo_upload_file(invalid_elo_pgn: str) -> UploadFile:
    """Create an UploadFile with invalid ELO data."""
    file_obj = io.BytesIO(invalid_elo_pgn.encode())
    return UploadFile(filename="invalid_elo_test.pgn", file=file_obj)


@pytest.fixture
def test_train_csv_path() -> Generator[Path, None, None]:
    """Create a temporary path for train.csv during tests."""
    csv_path = Settings.UPLOAD_DIRECTORY / "test_train.csv"
    csv_path.unlink(missing_ok=True)
    yield csv_path
    csv_path.unlink(missing_ok=True)


@pytest.fixture
def test_model_path() -> Generator[Path, None, None]:
    """Create a temporary path for model file during tests."""
    model_path = Settings.MODEL_DIRECTORY / "test_model.joblib"
    model_path.unlink(missing_ok=True)
    yield model_path
    model_path.unlink(missing_ok=True)


@pytest.fixture
def sample_train_csv() -> pl.DataFrame:
    """Create a sample training DataFrame with proper structure."""
    return pl.DataFrame({
        "Event": ["Blitz", "Blitz", "Rapid"],
        "Result": [1, -1, 0],
        "WhiteElo": [2045, 1576, 2315],
        "BlackElo": [2126, 1588, 2282],
        "ECO": ["B56", "A00", "E00"],
        "Opening": ["Sicilian Defense", "Hungarian Opening", "Catalan Opening"],
        "TimeControl": ["300+0", "180+0", "180+0"],
        "Termination": ["Normal", "Normal", "Normal"],
        "white_material": [38, 38, 38],
        "black_material": [38, 37, 38],
        "material_diff": [0, 1, 0],
        "white_pieces_attacked": [3, 1, 4],
        "white_attacked_value": [7, 1, 6],
        "black_pieces_attacked": [4, 3, 3],
        "black_attacked_value": [8, 5, 5],
        "attacked_diff": [1, 4, -1],
        "white_center_pieces": [1, 0, 1],
        "black_center_pieces": [1, 1, 2],
        "white_center_control": [3, 4, 4],
        "black_center_control": [3, 3, 4],
        "center_control_diff": [0, 1, 0],
        "white_extended_control": [12, 14, 10],
        "black_extended_control": [11, 9, 10],
        "extended_control_diff": [1, 5, 0],
        "white_mobility": [45, 46, 40],
        "black_mobility": [42, 33, 38],
        "mobility_diff": [3, 13, 2],
        "white_weighted_mobility": [195.0, 185.0, 142.0],
        "black_weighted_mobility": [0.0, 0.0, 0.0],
        "weighted_mobility_diff": [195.0, 185.0, 142.0],
        "position_advantage": [-1, 6, -4],
        "center_advantage": [1, 5, 0],
        "aggression": [1, 2, -1],
        "pawn_structure": [-2, 0, 0],
        "pieces_protected": [-2, 0, -1],
        "degrees_of_freedom": [3, 13, 2],
        "opponent_aggression": [3, 5, -3],
        "queen_position": [4, 5, 0],
        "knight_position": [0, 0, 2],
        "bishop_position": [-1, 1, -2],
        "rook_position": [2, 0, -3],
        "pawn_position": [0, 0, 0],
        "dof_x_material": [3306.0, 2969.0, 2964.0],
    })


@pytest.fixture
def sample_train_csv_file(
    sample_train_csv: pl.DataFrame,
    test_train_csv_path: Path,
) -> Path:
    """Save sample training CSV to temporary file."""
    sample_train_csv.write_csv(test_train_csv_path)
    return test_train_csv_path


@pytest.fixture(autouse=True)
def cleanup_test_files() -> Generator[None, None, None]:
    """Clean up any test files created during testing."""
    yield

    # Clean up test files
    test_files = [
        Settings.UPLOAD_DIRECTORY / "test_train.csv",
        Settings.UPLOAD_DIRECTORY / "train.csv",
        Settings.MODEL_DIRECTORY / "test_model.joblib",
        Settings.MODEL_DIRECTORY / "model.joblib",
    ]

    for file_path in test_files:
        file_path.unlink(missing_ok=True)
