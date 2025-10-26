from dataclasses import dataclass, field

import chess


@dataclass
class FeatureEngineerConfig:
    """Configuration for feature engineering."""

    move_number: int = 15  # Which move to analyze (full move number)
    piece_values: dict[int, int] = field(
        default_factory=lambda: {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0,
        }
    )
    center_squares: list[int] = field(
        default_factory=lambda: [chess.D4, chess.E4, chess.D5, chess.E5]
    )
    extended_center_squares: list[int] = field(
        default_factory=lambda: [
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
    )
