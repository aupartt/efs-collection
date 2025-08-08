from pydantic import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # RabbitMQ
    RABBITMQ_URL: AmqpDsn = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_DATA_QUEUE: str = "processed_data"

    # Database
    POSTGRES_URL: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/collecte"
    )

    REGION_NAME: str = "Bretagne"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
