from enum import IntEnum

import pandera as pa
import pandera.polars as ppl
from pandera.typing import Series


class GameResult(IntEnum):
    """Chess game results: -1 = Black wins, 0 = Draw, 1 = White wins"""

    BLACK_WINS = -1
    DRAW = 0
    WHITE_WINS = 1


class ChessGameSchema(ppl.DataFrameModel):
    """Schema for chess game training data validation."""

    # Player ratings (typically 400-3000+ for chess)
    whiteElo: Series[int] = pa.Field(
        ge=400,  # Minimum realistic rating
        le=4000,  # Maximum realistic rating (even for engines)
        description="White player's Elo rating",
    )

    blackElo: Series[int] = pa.Field(
        ge=400, le=4000, description="Black player's Elo rating"
    )

    # Game result must be one of the valid outcomes
    result: Series[int] = pa.Field(
        isin=[-1, 0, 1], description="Game result: -1=Black wins, 0=Draw, 1=White wins"
    )
