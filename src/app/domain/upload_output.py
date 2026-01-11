from pydantic import BaseModel, Field


class UploadServiceResponse(BaseModel):
    message: str = Field(description="Status message")
    total_features: int = Field(ge=0, description="Number of features")
    total_rows: int = Field(ge=0, description="Number of rows")
