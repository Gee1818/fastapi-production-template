import pandera as pa
import pandera.polars as ppl
from pandera.typing import Series

from .constants import ELOLimits


class ChessGameSchema(ppl.DataFrameModel):
    """Schema for chess game training data validation."""

    whiteElo: Series[int] = pa.Field(
        ge=ELOLimits.MIN,
        le=ELOLimits.MAX,
        description="White player's Elo rating",
    )

    blackElo: Series[int] = pa.Field(
        ge=ELOLimits.MIN, le=ELOLimits.MAX, description="Black player's Elo rating"
    )

    # Game result must be one of the valid outcomes
    result: Series[int] = pa.Field(
        isin=[-1, 0, 1], description="Game result: -1=Black wins, 0=Draw, 1=White wins"
    )
