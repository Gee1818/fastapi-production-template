import chess

# Filter configuration
TERMINATIONS = ["Normal"]
EVENTS = [
    "Rated Blitz game",
    "Rated Rapid game",
    "Rated Classical game",
]
ELO_RANGE = (1400, 2800)
MIN_MOVES = 15

# Mapping configuration
RESULT_MAP = {"1-0": 1, "0-1": -1, "1/2-1/2": 0}
EVENT_MAP = {
    "Rated Blitz game": "Blitz",
    "Rated Bullet game": "Bullet",
    "Rated Rapid game": "Rapid",
    "Rated Classical game": "Classical",
}

# Feature engineering configuration
MOVE_NUMBER = 15
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

CENTER_SQUARES = [
    chess.D4,
    chess.E4,
    chess.D5,
    chess.E5,
]

EXTENDED_CENTER_SQUARES = [
    chess.C3,
    chess.D3,
    chess.E3,
    chess.F3,
    chess.C4,
    chess.D4,
    chess.E4,
    chess.F4,
    chess.C5,
    chess.D5,
    chess.E5,
    chess.F5,
    chess.C6,
    chess.D6,
    chess.E6,
    chess.F6,
]

# Selection configuration

FEATURES_TO_DROP = [
    "Site",
    "Date",
    "Round",
    "White",
    "Black",
    "UTCDate",
    "UTCTime",
    "NumMoves",
    "Moves",
    "WhiteRatingDiff",
    "BlackRatingDiff",
]
