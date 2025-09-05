from pydantic import BaseModel
from datetime import datetime

class ScanInput(BaseModel):
    serial_no: str

class TestInput(BaseModel):
    serial_no: str
    test_type: str
    result: str

class TestResultResponse(TestInput):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
