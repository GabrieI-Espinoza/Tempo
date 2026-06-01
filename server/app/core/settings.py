from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parents[3] / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env"""

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    JWT_SECRET: str

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CORS_ORIGINS: list[str] = []

    PROJECT_NAME: str = "Tempo"

    # Override to False in production and manage schema changes with migrations
    GENERATE_SCHEMAS: bool = True

    ANTHROPIC_API_KEY: str = ""


settings = Settings()
