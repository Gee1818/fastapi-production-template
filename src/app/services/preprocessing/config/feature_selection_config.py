from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class SelectionConfig:
    features_to_drop: Sequence[str] = field(
        default_factory=lambda: [
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
    )
    target_feature: str = "Result"
