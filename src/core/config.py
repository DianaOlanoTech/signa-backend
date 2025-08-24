from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """
    Manages application settings and configurations.
    Loads environment variables from a .env file.
    """
    DATABASE_URL: str

    class Config:
        # Tell Pydantic to load the .env file from the backend's root directory.
        # This makes the configuration self-contained within the backend folder.
        env_file = BASE_DIR / ".env"

# Create a single, global instance of the settings.
settings = Settings()