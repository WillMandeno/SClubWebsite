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
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
