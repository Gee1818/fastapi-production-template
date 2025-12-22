from app.api.schema import BaseSchema


class UploadResponse(BaseSchema):
    message: str
    total_features: int
    total_rows: int
