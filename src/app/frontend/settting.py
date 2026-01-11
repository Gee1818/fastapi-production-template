from pydantic_settings import BaseSettings, SettingsConfigDict


class FrontendSettings(BaseSettings):
    API_ROOT_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(extra="ignore")

    @property
    def UPLOAD_API_URL(self) -> str:
        return f"{self.API_ROOT_URL}/upload/upload"

    @property
    def TRAIN_API_URL(self) -> str:
        return f"{self.API_ROOT_URL}/train/train"

    @property
    def HEALTH_API_URL(self) -> str:
        return f"{self.API_ROOT_URL}/health"
