from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class FilterConfig:
    terminations: Sequence[str] = field(default_factory=lambda: ("Normal"))
    events: Sequence[str] = field(
        default_factory=lambda: (
            "Rated Blitz game",
            "Rated Rapid game",
        )
    )
    elo_range: tuple[int, int] = field(default_factory=lambda: (1400, 2800))
    min_moves: int = 15
