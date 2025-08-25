from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )

    LOGGING_LEVEL: str = "INFO"
    ENVIRONMENT: str = "dev"

    # CLI SETUP
    REGION_NAME: str = "Bretagne"
    MIN_LAT: float = 47.09
    MAX_LAT: float = 49.06
    MIN_LNG: float = -5.42
    MAX_LNG: float = -0.93
    CRAWLER_BATCH: int = 20

    # POSTGRES
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "collecte"

    # LOKI
    LOKI_URL: str | None = None

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
