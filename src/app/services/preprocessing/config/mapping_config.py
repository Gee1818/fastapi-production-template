from dataclasses import dataclass, field


@dataclass
class MappingConfig:
    result_map: dict[str, int] = field(
        default_factory=lambda: {
            "1-0": 1,
            "0-1": -1,
            "1/2-1/2": 0,
        }
    )
    event_map: dict[str, str] = field(
        default_factory=lambda: {
            "Rated Blitz game": "Blitz",
            "Rated Bullet game": "Bullet",
            "Rated Rapid game": "Rapid",
            "Rated Classical game": "Classical",
        }
    )
