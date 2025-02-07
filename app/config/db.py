from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from env import settings

engine = create_engine(settings.database_url)
Base = declarative_base
SessionLocal = sessionmaker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close