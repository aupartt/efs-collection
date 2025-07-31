from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_urls_queue: str = "crawler_urls"
    rabbitmq_processed_data_queue: str = "processed_data"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()