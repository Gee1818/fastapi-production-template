from enum import IntEnum


class GameResult(IntEnum):
    """Chess game results: -1 = Black wins, 0 = Draw, 1 = White wins"""

    BLACK_WINS = -1
    DRAW = 0
    WHITE_WINS = 1
