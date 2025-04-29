import pytest
from backend.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_ping_route(client):
    response = client.post("/ping", json={"host": "8.8.8.8"})
    assert response.status_code == 200
    assert "output" in response.json

def test_history_route(client):
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json, list)
