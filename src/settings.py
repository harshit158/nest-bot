from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    telegram_bot_token: str
    openai_api_key: str
    
    # observability
    otel_exporter_otlp_endpoint: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()