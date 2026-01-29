from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file (backend/.env)
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)

# Database URL - prefer the value in backend/.env, otherwise fall back
# to a safe default (which will likely fail). If you see the fallback
# being used, check that backend/.env exists and contains DATABASE_URL.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/sclub_calendar",
)

# Create engine
# For local development (localhost/127.0.0.1) do not force SSL; require SSL for remote URLs
connect_args = {}
# If the DATABASE_URL references localhost/127.0.0.1, avoid forcing SSL for local development.
if 'localhost' not in DATABASE_URL and '127.0.0.1' not in DATABASE_URL:
    connect_args = {"sslmode": "require"}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
