from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel

from app.settings import Settings


class UploadService(BaseModel):
    upload_directory: Path = Settings.UPLOAD_DIRECTORY

    def save_file(self, file: UploadFile) -> dict[str, str | int]:

        file_path = self.upload_directory / "train.pgn"

        content = file.file.read()
        file_path.write_bytes(content)

        return {
            "size": len(content),
            "path": str(file_path),
        }
