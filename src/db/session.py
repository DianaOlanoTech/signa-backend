from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from pathlib import Path

# Get the backend project's root directory from our settings config.
project_root = Path(settings.Config.env_file).parent

# Extract the relative path of the database from the DATABASE_URL (e.g., './trademarks.db')
db_relative_path = settings.DATABASE_URL.split("///")[-1]

# Construct an absolute path to the database file.
# Example: C:\Users\YourName\Project\signa_backend\trademarks.db
absolute_db_path = project_root / db_relative_path

# Create the final, absolute database URL.
SQLALCHEMY_DATABASE_URL = f"sqlite:///{absolute_db_path}"

print(f"Database file location: {absolute_db_path}")


engine = create_engine(
    # Use the new absolute URL to connect to the database.
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