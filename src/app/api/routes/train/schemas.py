from app.api.schema import BaseSchema


class TrainResponse(BaseSchema):
    message: str = "Model trained successfully"
