from pydantic import AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_URL: AmqpDsn = "amqp://guest:guest@localhost:5672/"  # type: ignore[assignment] # noqa: E501, F722
    RABBITMQ_DATA_QUEUE: str = "processed_data"
    RABBITMQ_URLS_QUEUE: str = "crawler_urls"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
