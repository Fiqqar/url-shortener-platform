from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    base_url: str = "http://localhost:8000"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    max_body_bytes: int = Field(default=32768, gt=0)


settings = Settings()
