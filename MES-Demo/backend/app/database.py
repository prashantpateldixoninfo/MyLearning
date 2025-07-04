from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Read from Docker environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://mes_user:mes_pass@db:5432/mes_demo"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
