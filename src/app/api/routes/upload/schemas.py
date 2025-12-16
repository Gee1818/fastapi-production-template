from app.api.schema import BaseSchema


class UploadResponse(BaseSchema):
    message: str = "File uploaded successfully"
