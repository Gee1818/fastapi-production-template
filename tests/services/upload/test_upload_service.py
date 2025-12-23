import io

import pytest
from fastapi import UploadFile

from app.services.exceptions import DataValidationError
from app.services.upload import UploadService
from app.settings import Settings


def test_save_file_with_valid_pgn(
    upload_service: UploadService,
    valid_chess_data: str,
) -> None:
    """Test that save_file processes valid PGN data successfully."""
    file_obj = io.BytesIO(valid_chess_data.encode())
    upload_file = UploadFile(filename="test.pgn", file=file_obj)

    result = upload_service.save_file(upload_file)

    # Verify result structure
    assert "message" in result
    assert "totalFeatures" in result
    assert "totalRows" in result

    # Verify message content
    assert result["message"] == "Feature selection completed"

    # Verify numeric values
    assert isinstance(result["totalFeatures"], int)
    assert isinstance(result["totalRows"], int)
    assert result["totalFeatures"] > 0
    assert result["totalRows"] > 0

    # Verify train.csv was created
    train_file = Settings.UPLOAD_DIRECTORY / "train.csv"
    assert train_file.exists()


def test_save_file_with_invalid_elo(
    upload_service: UploadService,
    invalid_elo_data: str,
) -> None:
    """Test that save_file raises DataValidationError for invalid ELO ratings."""
    file_obj = io.BytesIO(invalid_elo_data.encode())
    upload_file = UploadFile(filename="invalid.pgn", file=file_obj)

    with pytest.raises(DataValidationError) as exc_info:
        upload_service.save_file(upload_file)

    assert "Data validation failed" in exc_info.value.message


def test_save_file_with_minimal_valid_game(
    upload_service: UploadService,
) -> None:
    """Test that save_file works with a minimal valid game."""
    minimal_pgn = """[Event "Rated Blitz game"]
[Site "https://lichess.org/test"]
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

    file_obj = io.BytesIO(minimal_pgn.encode())
    upload_file = UploadFile(filename="minimal.pgn", file=file_obj)

    result = upload_service.save_file(upload_file)

    # Should process successfully (might be 0 rows if filtered out)
    assert "message" in result
    assert "totalFeatures" in result
    assert "totalRows" in result
