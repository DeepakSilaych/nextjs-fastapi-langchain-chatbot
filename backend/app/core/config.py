from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "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")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "your-google-key-here")
    VECTORSTORE_DIR: str = "./data/vectorstore"
    UPLOAD_DIR: str = "./uploads"
    DATABASE_URL: str = "sqlite:///./app.db"
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"

settings = Settings()