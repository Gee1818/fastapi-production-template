from collections.abc import Sequence
from dataclasses import dataclass, field

from .config import FEATURES_TO_DROP


@dataclass
class SelectionConfig:
    features_to_drop: Sequence[str] = field(default_factory=lambda: FEATURES_TO_DROP)
    target_feature: str = "Result"
