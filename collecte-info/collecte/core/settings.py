from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    POSTGRES_URL: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/collecte"
    )

    REGION_NAME: str = "Bretagne"
    CRAWLER_BATCH: int = 20

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
