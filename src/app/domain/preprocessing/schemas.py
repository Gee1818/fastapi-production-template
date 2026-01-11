from pydantic import BaseModel, Field


class PreprocessingResult(BaseModel):
    message: str = Field(description="Status message of the operation")
    total_features: int = Field(ge=0, description="Number of features in the dataset")
    total_rows: int = Field(ge=0, description="Number of rows in the dataset")
