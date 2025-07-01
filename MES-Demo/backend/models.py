from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    serial_no = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    serial_no = Column(String, index=True)
    test_type = Column(String)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
