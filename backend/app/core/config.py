from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "your-openai-api-key"
    OPENROUTER_API_KEY: str = "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"
    VECTORSTORE_DIR: str = "./data/vectorstore"
    UPLOAD_DIR: str = "./uploads"
    DATABASE_URL: str = "sqlite:///./app.db"
    DEFAULT_MODEL: str = "openai/gpt-3.5-turbo"
    
    class Config:
        env_file = ".env"

settings = Settings()