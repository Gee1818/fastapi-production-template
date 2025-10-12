from collections.abc import Sequence
from typing import Protocol, Self, runtime_checkable

from numpy import ndarray
from polars import DataFrame, Series


@runtime_checkable
class MLModel(Protocol):
    def predict(
        self, X: Sequence[Sequence[float]]
    ) -> ndarray | tuple[ndarray, ndarray]: ...
    def fit(self, X: DataFrame, y: Series) -> Self: ...
