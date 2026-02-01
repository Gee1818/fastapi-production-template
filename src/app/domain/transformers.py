from typing import Self

import polars as pl
from sklearn.base import BaseEstimator, TransformerMixin

from app.domain.preprocessing.config import (
    FeatureEngineerConfig,
    FilterConfig,
    MappingConfig,
    SelectionConfig,
)
from app.domain.preprocessing.steps.feature_engineer import add_features
from app.domain.preprocessing.steps.feature_selection import select_features
from app.domain.preprocessing.steps.filter import apply_filters
from app.domain.preprocessing.steps.mapping import apply_mappings_features


class FilterTransformer(BaseEstimator, TransformerMixin):
    """Transformer to apply filtering to chess game data."""

    def __init__(self) -> None:
        self.filter_config = FilterConfig()

    def fit(self, _X: pl.DataFrame, _y: pl.Series | None = None) -> Self:
        return self

    def transform(self, X: pl.DataFrame) -> pl.DataFrame:
        return apply_filters(X, self.filter_config)


class MappingTransformer(BaseEstimator, TransformerMixin):
    """Transformer to apply mappings to chess game data."""

    def __init__(self) -> None:
        self.mapping_config = MappingConfig()

    def fit(self, _X: pl.DataFrame, _y: pl.Series | None = None) -> Self:
        return self

    def transform(self, X: pl.DataFrame) -> pl.DataFrame:
        return apply_mappings_features(X, self.mapping_config)


class FeatureEngineerTransformer(BaseEstimator, TransformerMixin):
    """Transformer to add engineered features to chess game data."""

    def __init__(self) -> None:
        self.feature_engineer_config = FeatureEngineerConfig()

    def fit(self, _X: pl.DataFrame, _y: pl.Series | None = None) -> Self:
        return self

    def transform(self, X: pl.DataFrame) -> pl.DataFrame:
        return add_features(X, self.feature_engineer_config)


class FeatureSelectionTransformer(BaseEstimator, TransformerMixin):
    """Transformer to select features and extract target variable."""

    def __init__(self) -> None:
        self.selection_config = SelectionConfig()
        self.target_: pl.Series | None = None

    def fit(self, _X: pl.DataFrame, _y: pl.Series | None = None) -> Self:
        return self

    def transform(self, X: pl.DataFrame) -> pl.DataFrame:
        self.target_ = X[self.selection_config.target_feature]
        return select_features(X, self.selection_config)
