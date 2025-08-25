from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from pathlib import Path

# Check if we're using PostgreSQL (production) or SQLite (development)
if settings.DATABASE_URL.startswith("postgresql://"):
    # Production: Use PostgreSQL directly
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    print(f"Using PostgreSQL database: {settings.DATABASE_URL}")

    # PostgreSQL connection arguments
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

else:
    # Development: Use SQLite with absolute path
    # Get the backend project's root directory from our settings config.
    project_root = Path(settings.Config.env_file).parent

    # Extract the relative path of the database from the DATABASE_URL (e.g., './trademarks.db')
    db_relative_path = settings.DATABASE_URL.split("///")[-1]

    # Construct an absolute path to the database file.
    absolute_db_path = project_root / db_relative_path

    # Create the final, absolute database URL for SQLite.
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{absolute_db_path}"
    print(f"Using SQLite database file: {absolute_db_path}")

    # SQLite connection arguments
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()