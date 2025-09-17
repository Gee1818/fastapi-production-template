from typing import List, Self  # noqa: UP035

from pydantic import model_validator

from app.api.schema import BaseSchema
from app.services.training import DimensionalityMismatchError


class Features(BaseSchema):
    whiteElo: int
    blackElo: int


class TrainRequest(BaseSchema):
    features: List[Features]  # noqa: UP006
    result: List[int]  # noqa: UP006

    @model_validator(mode="after")
    def features_and_labels_have_same_length(self) -> Self:
        if len(self.features) != len(self.result):
            raise DimensionalityMismatchError(
                x_dim=len(self.features),
                y_dim=len(self.result),
            )
        return self


class TrainResponse(BaseSchema):
    message: str = "Model trained successfully"
