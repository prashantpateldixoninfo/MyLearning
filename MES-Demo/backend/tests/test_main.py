import pytest
from httpx import AsyncClient
from app.main import app
from unittest.mock import MagicMock
from fastapi import Depends
from app.database import get_db  # <-- this must be imported in main.py too

# Override get_db with a mock
async def override_get_db():
    mock_session = MagicMock()
    yield mock_session

# Register the mock
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "MES-Demo API is live"}

@pytest.mark.asyncio
async def test_post_barcode():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "barcode": "PRD00123456",
            "timestamp": "2025-07-06T14:30:00Z",
            "result": "PASS"
        }
        response = await ac.post("/barcode", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "received" in data["message"].lower()
