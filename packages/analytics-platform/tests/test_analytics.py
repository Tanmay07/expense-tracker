import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers():
    res = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

def test_semantic_metric_evaluation():
    headers = get_auth_headers()
    
    # 1. Register a Semantic Metric
    res1 = client.post("/api/v1/analytics/metrics", json={
        "metric_id": "savings_rate",
        "name": "Personal Savings Rate",
        "formula": "(Income - Expenses) / Income",
        "units": "percentage",
        "owner": "system"
    }, headers=headers)
    assert res1.status_code == 200
    
    # 2. Evaluate the Metric
    res2 = client.post("/api/v1/analytics/evaluate", params={
        "metric_id": "savings_rate"
    }, json={
        "income": 10000.0,
        "expenses": 6000.0
    }, headers=headers)
    
    assert res2.status_code == 200
    data = res2.json()
    assert data["metric_id"] == "savings_rate"
    assert data["value"] == 0.4  # (10000 - 6000) / 10000 = 0.4 (40%)
