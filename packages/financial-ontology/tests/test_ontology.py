import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers():
    res = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.skip(reason="Pending package implementation")
def test_ontology_concept_retrieval():
    headers = get_auth_headers()
    
    # 1. Fetch the exact canonical concept
    res1 = client.get("/api/v1/ontology/concepts/concept_account", headers=headers)
    assert res1.status_code == 200
    data = res1.json()
    assert data["name"] == "Account"
    assert data["business_name"] == "Financial Account"

@pytest.mark.skip(reason="Pending package implementation")
def test_ontology_alias_resolution():
    headers = get_auth_headers()
    
    # 1. An AI Agent asks for "wallet", the OS should resolve it to "Account"
    res1 = client.get("/api/v1/ontology/search?alias=wallet", headers=headers)
    assert res1.status_code == 200
    data = res1.json()
    assert data["id"] == "concept_account"
    assert data["name"] == "Account"
    
    # 2. An AI Agent asks for "wealth", the OS should resolve it to "Net Worth"
    res2 = client.get("/api/v1/ontology/search?alias=wealth", headers=headers)
    assert res2.status_code == 200
    assert res2.json()["id"] == "concept_net_worth"
