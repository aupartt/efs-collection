from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./app/.env", case_sensitive=False, extra="ignore")

    LOGGING_LEVEL: str = "INFO"
    ENVIRONMENT: str = "dev"

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
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # STREAMLIT
    ST_SESSION_STATE: dict = {
        "limit": None,
        "selected_locations": [],
        "collect_types": {
            "blood": {"fr": "sang", "en": "blood", "short": "st"},
            "plasma": {"fr": "plasma", "en": "plasma", "short": "pla"},
            "platelet": {"fr": "plaquette", "en": "platelet", "short": "cpa"},
        },
    }


settings = Settings()
