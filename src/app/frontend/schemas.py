from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    message: str = Field(description="Status message")
    total_features: int = Field(
        alias="totalFeatures", ge=0, description="Number of features"
    )
    total_rows: int = Field(alias="totalRows", ge=0, description="Number of rows")

    class Config:
        populate_by_name = True  # Allow both snake_case and camelCase


class TrainResponse(BaseModel):
    message: str = Field(description="Training status message")

    class Config:
        populate_by_name = True
