from fastapi import UploadFile
from pandera.errors import SchemaError
from pydantic import BaseModel

from app.domain import ReadFileServiceResponse
from app.domain.chess_game import ChessGameSchema
from app.domain.read_pgn import read_pgn
from app.services.exceptions import DataValidationError
from app.settings import Settings


class ReadFileService(BaseModel):
    @staticmethod
    def read_pgn(file: UploadFile) -> ReadFileServiceResponse:
        df = read_pgn(file)

        try:
            ChessGameSchema.validate(df)
        except SchemaError as e:
            raise DataValidationError(message=f"Data validation failed: {e!s}") from e

        df.write_csv(Settings.UPLOAD_DIRECTORY / "train.csv")

        return ReadFileServiceResponse(
            message="Feature selection completed",
            total_features=df.shape[1],
            total_rows=df.shape[0],
        )
