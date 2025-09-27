from typing import Any, Protocol, Self, runtime_checkable

from polars import DataFrame, Series


@runtime_checkable
class MLModel(Protocol):
    def predict(self, X: Any, **kwargs: Any) -> Any: ...
    def fit(self, X: DataFrame, y: Series) -> Self: ...
