import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers():
    res = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.skip(reason="Pending package implementation")
def test_semantic_query_and_lineage():
    headers = get_auth_headers()
    
    # 1. Execute a Semantic Query for Savings Rate
    # The DAG will resolve Savings Rate -> Savings (Income - Expenses) / Income
    res1 = client.post("/api/v1/semantic/query", params={
        "metric_id": "savings_rate"
    }, json={
        "income": 10000.0,
        "expenses": 6000.0
    }, headers=headers)
    
    assert res1.status_code == 200
    data = res1.json()
    assert data["metric_id"] == "savings_rate"
    assert data["value"] == 0.4
    
    query_id = data["query_id"]
    assert query_id is not None
    
    # 2. Fetch Lineage for AI Explainability
    res2 = client.get(f"/api/v1/semantic/lineage/{query_id}", headers=headers)
    assert res2.status_code == 200
    lineage = res2.json()
    
    # The Savings Rate DAG node explicitly depends on ["savings", "income"]
    assert "savings" in lineage["dependencies_resolved"]
    assert "income" in lineage["dependencies_resolved"]
    assert "postgres.ledger_entries" in lineage["raw_tables_scanned"]
