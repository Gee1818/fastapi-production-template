from app.api.schema import BaseSchema


class PredictionResponse(BaseSchema):
    result: str = "Prediction completed successfully"
