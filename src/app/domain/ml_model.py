from typing import Any, Protocol, Self, runtime_checkable

import numpy as np
from numpy.typing import NDArray
from polars import DataFrame, Series


@runtime_checkable
class MLModel(Protocol):
    def predict_proba(self, X: DataFrame) -> NDArray[np.float64]: ...

    def fit(self, X: DataFrame, y: Series) -> Self: ...


class SKLearnModelAdapter:
    """Adapter to make sklearn models compatible with MLModel protocol."""

    def __init__(self, model: Any) -> None:
        self._model = model

    def predict_proba(self, X: DataFrame) -> Any:
        return self._model.predict_proba(X)

    def fit(self, X: DataFrame, y: Series) -> Self:
        self._model.fit(X, y)
        return self
