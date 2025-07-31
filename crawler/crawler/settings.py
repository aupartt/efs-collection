from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_urls_queue: str = "crawler_urls"
    rabbitmq_processed_data_queue: str = "processed_data"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()