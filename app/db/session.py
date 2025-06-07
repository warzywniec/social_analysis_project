# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Możesz zmienić na PostgreSQL np. "postgresql://user:pass@localhost/db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# SQLite: trzeba dodać check_same_thread
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Factory do tworzenia sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazowa klasa dla modeli ORM
Base = declarative_base()

# Dependency do FastAPI – injekcja sesji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
