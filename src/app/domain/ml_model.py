from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MLModel(Protocol):
    def predict(self, X: Any, **kwargs: Any) -> Any: ...
    def fit(self, X: Any, y: Any, **kwargs: Any) -> Any: ...
