from pydantic import Field

from app.api.schema import BaseSchema


class ReadPGNResponse(BaseSchema):
    message: str = Field(description="Status message")
    total_features: int = Field(ge=0, description="Number of features")
    total_rows: int = Field(ge=0, description="Number of rows")
