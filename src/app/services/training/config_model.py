from dataclasses import dataclass
from typing import Literal


@dataclass
class ModelConfig:
    # RandomForestClassifier parameters
    n_estimators: int = 100
    max_depth: int = 10
    min_samples_leaf: int = 2
    max_features: Literal["sqrt", "log2"] | float = "sqrt"
    min_samples_split: int = 80
    max_samples: float = 0.5
    random_state: int = 42
