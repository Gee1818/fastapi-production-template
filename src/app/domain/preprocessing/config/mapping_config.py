from dataclasses import dataclass, field

from .config import EVENT_MAP, RESULT_MAP


@dataclass
class MappingConfig:
    result_map: dict[str, int] = field(default_factory=lambda: RESULT_MAP)
    event_map: dict[str, str] = field(default_factory=lambda: EVENT_MAP)
