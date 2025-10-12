from dataclasses import dataclass
from enum import IntEnum


class GameResult(IntEnum):
    """Chess game results: -1 = Black wins, 0 = Draw, 1 = White wins"""

    BLACK_WINS = -1
    DRAW = 0
    WHITE_WINS = 1


@dataclass
class ELOLimits:
    """Elo rating limits for chess players."""

    MIN: int = 400
    MAX: int = 4000
