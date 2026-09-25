"""
SmritiSaathi — Application Configuration

Reads all settings from environment variables (.env file).
Uses the local PostgreSQL configuration when configured, but falls back to SQLite so the
project can start cleanly in a lightweight local development environment.
"""

import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


def _default_database_url() -> str:
    """Prefer PostgreSQL for local development, but keep SQLite as a safe fallback."""
    configured = os.getenv("DATABASE_URL")
    if configured:
        return configured
    return "sqlite+aiosqlite:///./smritisaathi.db"


def _default_database_url_sync() -> str:
    configured = os.getenv("DATABASE_URL_SYNC")
    if configured:
        return configured
    return "sqlite:///./smritisaathi.db"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_ENV: str = "development"
    APP_NAME: str = "SmritiSaathi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = Field(default_factory=_default_database_url)
    DATABASE_URL_SYNC: str = Field(default_factory=_default_database_url_sync)

    # JWT Authentication
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174"

    # File uploads
    UPLOAD_DIR: str = "./uploads"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
