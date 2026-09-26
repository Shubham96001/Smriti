from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmritiSaathi"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = False
    database_url_raw: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/smritisaathi",
        validation_alias=AliasChoices("DATABASE_URL", "DATABASE_URL_RAW"),
    )
    jwt_secret_key: str = "change-this-development-secret-to-a-long-random-value"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:
        return self.database_url_raw.replace("postgresql+asyncpg://", "postgresql://").replace(
            "postgres+asyncpg://", "postgresql://"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()