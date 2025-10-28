from .feature_engineer_config import FeatureEngineerConfig
from .feature_selection_config import SelectionConfig
from .filter_config import FilterConfig
from .mapping_config import MappingConfig

filter_config: FilterConfig = FilterConfig(
    terminations=["Normal"],
    events=[
        "Rated Blitz game",
        "Rated Rapid game",
        "Rated Classical game",
    ],
    elo_range=(1400, 2800),
    min_moves=15,
)

feature_engineer_config: FeatureEngineerConfig = FeatureEngineerConfig()
mapping_config: MappingConfig = MappingConfig()
selection_config: SelectionConfig = SelectionConfig()
