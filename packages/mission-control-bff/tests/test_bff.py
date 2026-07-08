from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mission-control-bff"}


def test_get_dashboard():
    response = client.get("/api/bff/dashboard", headers={"mock_user_123": "true"})
    assert response.status_code == 200
    data = response.json()
    assert "mission_status" in data
    assert "net_worth" in data
    assert "upcoming_actions" in data


def test_get_missions():
    response = client.get("/api/bff/missions", headers={"mock_user_123": "true"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "progress" in data[0]


def test_get_graph():
    response = client.get("/api/bff/graph", headers={"mock_user_123": "true"})
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
