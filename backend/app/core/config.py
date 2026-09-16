from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Architect Portfolio API"
    app_env: str = "development"
    debug: bool = True

    frontend_url: str = "http://localhost:5173"
    FRONTEND_URL: str = "http://localhost:5173"

    DATABASE_URL: str = ""

    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_STORAGE_BUCKET: str = ""

    RESEND_API_KEY: str = ""
    INQUIRY_NOTIFICATION_EMAIL: str = ""
    RESEND_FROM_EMAIL: str = "onboarding@resend.dev"

    firebase_project_id: str = "demo-project"
    firebase_client_email: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_credentials_path: str = "firebase-key.json"

    supabase_storage_bucket: str = "portfolio"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()