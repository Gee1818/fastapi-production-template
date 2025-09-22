from typing import Protocol, Self, runtime_checkable

import polars as pl


@runtime_checkable
class MLModel(Protocol):
    def predict(self, X: pl.DataFrame) -> pl.Series: ...

    def fit(self, X: pl.DataFrame, y: pl.Series) -> Self: ...
