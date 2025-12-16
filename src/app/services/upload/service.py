from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel

from app.settings import Settings


class UploadService(BaseModel):
    upload_directory: Path = Settings.UPLOAD_DIRECTORY

    def save_file(self, file: UploadFile) -> dict[str, str | int]:

        temp_error = "File must have a filename"
        if not file.filename:
            raise ValueError(temp_error)
        file_path = self.upload_directory / file.filename

        content = file.file.read()
        file_path.write_bytes(content)

        return {
            "filename": file.filename,
            "size": len(content),
            "path": str(file_path),
        }
