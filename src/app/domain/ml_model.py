from typing import Protocol, Self, runtime_checkable

from polars import DataFrame, Series


@runtime_checkable
class MLModel(Protocol):
    def predict_proba(self, X: DataFrame) -> Self: ...

    def fit(self, X: DataFrame, y: Series) -> Self: ...
