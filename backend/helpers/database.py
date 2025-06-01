from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency function that provides a database session.
    This function is typically used with FastAPI's dependency injection system
    to provide a scoped database session to route handlers. It ensures that the
    database session is properly opened and closed, preventing resource leaks.
    Yields:
        Session: A SQLAlchemy database session object.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()