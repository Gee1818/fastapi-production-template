from pydantic import BaseModel, ConfigDict, Field


class UploadResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    message: str = Field(description="Status message")
    total_features: int = Field(
        alias="totalFeatures", ge=0, description="Number of features"
    )
    total_rows: int = Field(alias="totalRows", ge=0, description="Number of rows")


class TrainResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(description="Training status message")
