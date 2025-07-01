from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import SessionLocal, engine, Base
from models import Product, TestResult
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from local file frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ['file://', 'http://localhost:5500'] if hosting with live server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

class ScanInput(BaseModel):
    serial_no: str

class TestInput(BaseModel):
    serial_no: str
    test_type: str
    result: str

@app.post("/scan")
def scan_product(scan: ScanInput):
    db = SessionLocal()
    new_product = Product(serial_no=scan.serial_no)
    db.add(new_product)
    db.commit()
    return {"message": "Product scanned", "serial_no": scan.serial_no}

@app.post("/test")
def add_test_result(test: TestInput):
    db = SessionLocal()
    new_test = TestResult(**test.dict())
    db.add(new_test)
    db.commit()
    return {"message": "Test result recorded"}

@app.get("/dashboard")
def get_dashboard():
    db = SessionLocal()
    results = db.query(TestResult).all()
    return results
