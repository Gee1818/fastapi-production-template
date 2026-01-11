from collections.abc import Sequence
from dataclasses import dataclass, field

from .config import ELO_RANGE, EVENTS, MIN_MOVES, TERMINATIONS


@dataclass
class FilterConfig:
    terminations: Sequence[str] = field(default_factory=lambda: TERMINATIONS)
    events: Sequence[str] = field(default_factory=lambda: EVENTS)
    elo_range: tuple[int, int] = field(default_factory=lambda: ELO_RANGE)
    min_moves: int = MIN_MOVES
