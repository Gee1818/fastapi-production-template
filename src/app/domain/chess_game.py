import pandera as pa
import pandera.polars as ppl
from pandera.typing import Series

from .constants import ELOLimits


class ChessGameSchema(ppl.DataFrameModel):
    """Schema for chess game training data validation."""

    Event: Series[str] = pa.Field()
    Site: Series[str] = pa.Field()
    Date: Series[str] = pa.Field()
    Round: Series[str] = pa.Field()
    White: Series[str] = pa.Field()
    Black: Series[str] = pa.Field()
    Result: Series[str] = pa.Field()
    UTCDate: Series[str] = pa.Field()
    UTCTime: Series[str] = pa.Field()
    WhiteElo: Series[int] = pa.Field(ge=ELOLimits.MIN, le=ELOLimits.MAX)
    BlackElo: Series[int] = pa.Field(ge=ELOLimits.MIN, le=ELOLimits.MAX)
    WhiteRatingDiff: Series[str] = pa.Field()
    BlackRatingDiff: Series[str] = pa.Field()
    ECO: Series[str] = pa.Field()
    Opening: Series[str] = pa.Field()
    TimeControl: Series[str] = pa.Field()
    Termination: Series[str] = pa.Field()
    Moves: Series[str] = pa.Field()
    NumMoves: Series[int] = pa.Field(ge=0)
