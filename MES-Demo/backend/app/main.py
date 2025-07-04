from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal, engine, Base
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection for DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/scan")
def scan_product(scan: schemas.ScanInput, db: Session = Depends(get_db)):
    new_product = models.Product(serial_no=scan.serial_no)
    db.add(new_product)
    db.commit()
    return {"message": "Product scanned", "serial_no": scan.serial_no}

@app.post("/test")
def add_test_result(test: schemas.TestInput, db: Session = Depends(get_db)):
    new_test = models.TestResult(**test.dict())
    db.add(new_test)
    db.commit()
    return {"message": "Test result recorded"}

@app.get("/dashboard", response_model=list[schemas.TestResultResponse])
def get_dashboard(db: Session = Depends(get_db)):
    return db.query(models.TestResult).all()
