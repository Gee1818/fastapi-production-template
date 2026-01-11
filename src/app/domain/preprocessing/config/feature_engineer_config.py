from dataclasses import dataclass, field

from .config import CENTER_SQUARES, EXTENDED_CENTER_SQUARES, MOVE_NUMBER, PIECE_VALUES


@dataclass
class FeatureEngineerConfig:
    """Configuration for feature engineering."""

    move_number: int = MOVE_NUMBER
    piece_values: dict[int, int] = field(default_factory=lambda: PIECE_VALUES)
    center_squares: list[int] = field(default_factory=lambda: CENTER_SQUARES)
    extended_center_squares: list[int] = field(
        default_factory=lambda: EXTENDED_CENTER_SQUARES
    )
