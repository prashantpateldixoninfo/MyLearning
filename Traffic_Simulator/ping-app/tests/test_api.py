import pytest
from backend.app import app
from unittest.mock import patch
from pymongo import MongoClient, errors

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Mocked version of the insert_ping function
@patch("backend.app.insert_ping")
def test_ping_route_mock(mock_insert, client):
    mock_insert.return_value = None  # No need to return anything
    response = client.post("/ping", json={"host": "8.8.8.8"})
    assert response.status_code == 200
    assert "output" in response.json
    assert isinstance(response.json["output"], str)
    mock_insert.assert_called_once()  # Ensure insert was called

# Mocked version of the fetch_history function
@patch("backend.app.fetch_history")
def test_history_route_all_mock(mock_fetch, client):
    mock_fetch.return_value = [
        {"host": "8.8.8.8", "output": "PING 8.8.8.8 ..."},
        {"host": "1.1.1.1", "output": "PING 1.1.1.1 ..."}
    ]
    response = client.post("/history", json={})
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2

@patch("backend.app.fetch_history")
def test_history_route_with_host_mock(mock_fetch, client):
    mock_fetch.return_value = [
        {"host": "8.8.8.8", "output": "PING 8.8.8.8 ..."}
    ]
    response = client.post("/history", json={"host": "8.8.8.8"})
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1
    assert response.json[0]["host"] == "8.8.8.8"

# Helper to check MongoDB availability
def mongodb_available():
    try:
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=200)
        client.admin.command("ping")  # Better than server_info for a quick check
        print("MongoDB is available")
        return True
    except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure, errors.PyMongoError) as e:
        print(f"MongoDB is not available: {e}")
        return False


# --- Ping Route Test ---
def test_ping_route(client):
    if mongodb_available():
        response = client.post("/ping", json={"host": "8.8.8.8"})
    else:
        with patch("backend.app.insert_ping") as mock_insert:
            mock_insert.return_value = None
            response = client.post("/ping", json={"host": "8.8.8.8"})
            mock_insert.assert_called_once()
    assert response.status_code == 200
    assert "output" in response.json
    assert isinstance(response.json["output"], str)

# --- History Route Test (No host) ---
def test_history_route_all(client):
    if mongodb_available():
        response = client.post("/history", json={})
    else:
        with patch("backend.app.fetch_history") as mock_fetch:
            mock_fetch.return_value = [
                {"host": "8.8.8.8", "output": "PING 8.8.8.8 ..."},
                {"host": "1.1.1.1", "output": "PING 1.1.1.1 ..."},
            ]
            response = client.post("/history", json={})
    assert response.status_code == 200
    assert isinstance(response.json, list)

# --- History Route Test (With host) ---
def test_history_route_with_host(client):
    if mongodb_available():
        response = client.post("/history", json={"host": "8.8.8.8"})
    else:
        with patch("backend.app.fetch_history") as mock_fetch:
            mock_fetch.return_value = [
                {"host": "8.8.8.8", "output": "PING 8.8.8.8 ..."}
            ]
            response = client.post("/history", json={"host": "8.8.8.8"})
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for record in response.json:
        assert "host" in record
        assert record["host"] == "8.8.8.8"
