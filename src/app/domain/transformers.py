import polars as pl
from sklearn.base import BaseEstimator, TransformerMixin

from app.domain.preprocessing.config import (
    FilterConfig,
)
from app.domain.preprocessing.steps.filter import apply_filters


class FilterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:

        self.config = FilterConfig()

    def fit(self, X: pl.DataFrame, y: pl.Series) -> "FilterTransformer":

        return self

    def transform(self, X: pl.DataFrame) -> pl.DataFrame:
        return apply_filters(X, self.config)
