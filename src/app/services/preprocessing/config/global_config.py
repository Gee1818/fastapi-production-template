from dataclasses import dataclass, field

from .feature_engineer_config import FeatureEngineerConfig
from .feature_selection_config import SelectionConfig
from .filter_config import FilterConfig
from .mapping_config import MappingConfig


@dataclass
class GlobalConfig:
    filter_config: FilterConfig = field(default_factory=FilterConfig)
    feature_engineer_config: FeatureEngineerConfig = field(
        default_factory=FeatureEngineerConfig
    )
    selection_config: SelectionConfig = field(default_factory=SelectionConfig)
    mapping_config: MappingConfig = field(default_factory=MappingConfig)
