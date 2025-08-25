import os
from pathlib import Path
from pydantic_settings import BaseSettings

# The base directory is the root of the backend project.
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """ Manages application settings and configurations. """

    # This will be populated by Render's environment variable directly.
    # We set a default for local development.
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'trademarks.db'}"

    # We can detect the environment based on the presence of the RENDER variable.
    ENVIRONMENT: str = "production" if os.getenv("RENDER") else "development"

    class Config:
        # Load a .env file if it exists (for local development).
        env_file = BASE_DIR / ".env"
        # Make sure environment variable names are matched case-sensitively.
        case_sensitive = True

    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database."""
        return self.DATABASE_URL.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        """Check if using PostgreSQL or Postgres database."""
        return self.DATABASE_URL.startswith("postgresql") or self.DATABASE_URL.startswith("postgres")


# Create a single, global instance of the settings.
settings = Settings()

# A print statement to help debug which environment is being used.
print(f"--- SETTINGS LOADED ---")
print(f"Environment: {settings.ENVIRONMENT}")
print(f"Database Type: {'PostgreSQL' if settings.is_postgres else 'SQLite'}")
print(f"Database URL Hint: {settings.DATABASE_URL[:30]}...")
print(f"-----------------------")