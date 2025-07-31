from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_DATA_QUEUE: str = "processed_data"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()