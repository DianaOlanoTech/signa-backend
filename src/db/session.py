from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.core.config import settings


def create_database_engine():
    """Create database engine with appropriate configuration"""

    if settings.is_sqlite:
        # SQLite configuration
        engine = create_engine(
            settings.DATABASE_URL,
            poolclass=StaticPool,
            connect_args={
                "check_same_thread": False,
                "timeout": 20,
            },
            echo=False,  # Set to True for SQL debugging
        )

        # Enable foreign keys for SQLite
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    elif settings.is_postgres:
        # PostgreSQL configuration
        engine = create_engine(
            settings.DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,  # Set to True for SQL debugging
        )
    else:
        raise ValueError(f"Unsupported database URL: {settings.DATABASE_URL}")

    return engine


# Create engine and session factory
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database dependency for FastAPI endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
