from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Agentic Operations Intelligence Platform"
    app_version: str = "1.0.0"
    environment: str = "local"

    database_url: str = "sqlite:///./agentic_ops.db"

    confidence_threshold: float = 0.70
    human_review_threshold: float = 0.65

    class Config:
        env_file = ".env"


settings = Settings()