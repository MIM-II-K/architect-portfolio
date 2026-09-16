from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Architect Portfolio API"
    app_env: str = "development"
    debug: bool = True

    frontend_url: str = "http://localhost:5173"

    firebase_project_id: str
    firebase_client_email: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_credentials_path: str = "firebase-key.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()