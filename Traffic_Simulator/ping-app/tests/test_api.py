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
    assert isinstance(response.json["output"], str)

def test_history_route_all(client):
    # No host filter – should return all records
    response = client.post("/history", json={})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_history_route_with_host(client):
    # With host filter – should return only matching records
    response = client.post("/history", json={"host": "8.8.8.8"})
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for record in response.json:
        assert "host" in record
        assert record["host"] == "8.8.8.8"
