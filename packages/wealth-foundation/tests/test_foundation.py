import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers():
    return {"Authorization": "Bearer password123"}

def test_wealth_foundation_step1():
    headers = get_auth_headers()
    
    # 1. Create Household
    h_res = client.post("/api/v1/foundation/households", json={
        "name": "Smith Family",
        "base_currency": "USD"
    }, headers=headers)
    assert h_res.status_code == 200
    household_id = h_res.json()["id"]
    
    # 2. Add Member (Spouse)
    m_res = client.post(f"/api/v1/foundation/households/{household_id}/members", json={
        "name": "Jane Smith",
        "role": "SPOUSE",
        "ownership_percentage": 50.0
    }, headers=headers)
    assert m_res.status_code == 200
    assert m_res.json()["role"] == "SPOUSE"
    
    # 3. FX Convert (USD to EUR)
    fx_res = client.get("/api/v1/foundation/fx/convert?amount=1000&base=USD&target=EUR", headers=headers)
    assert fx_res.status_code == 200
    assert fx_res.json()["converted_amount"] == 900.0 # 1000 * 0.9 mock rate
    
    
    # 4. FX Convert (Unsupported)
    bad_fx = client.get("/api/v1/foundation/fx/convert?amount=1000&base=USD&target=JPY", headers=headers)
    assert bad_fx.status_code == 400

def test_wealth_foundation_step2():
    headers = get_auth_headers()
    
    # 1. Announce Corporate Action (Stock Split)
    ca_res = client.post("/api/v1/foundation/corporate-actions", json={
        "asset_symbol": "NVDA",
        "action_type": "SPLIT",
        "ratio": 10.0
    }, headers=headers)
    assert ca_res.status_code == 200
    assert ca_res.json()["action_type"] == "SPLIT"
    assert ca_res.json()["ratio"] == 10.0
    assert ca_res.json()["status"] == "PENDING"
    
    # 2. Link Goal Funding
    gf_res = client.post("/api/v1/foundation/goal-funding", json={
        "goal_id": "goal-retirement-123",
        "asset_id": "port-456",
        "allocation_percentage": 100.0,
        "priority": 1
    }, headers=headers)
    assert gf_res.status_code == 200
    assert gf_res.json()["goal_id"] == "goal-retirement-123"
    assert gf_res.json()["asset_id"] == "port-456"

def test_wealth_foundation_step3():
    headers = get_auth_headers()
    
    # 1. Register Provider
    prov_res = client.post("/api/v1/foundation/providers", json={
        "name": "YAHOO_FINANCE",
        "provider_type": "MARKET_DATA",
        "priority": 1,
        "capabilities": ["REALTIME_QUOTES"]
    }, headers=headers)
    assert prov_res.status_code == 200
    assert prov_res.json()["name"] == "YAHOO_FINANCE"
    
    # 2. Log Explanation
    exp_res = client.post("/api/v1/foundation/explain", json={
        "recommendation_id": "rec-999",
        "rule_applied": "Tax Loss Harvesting",
        "confidence_score": 0.95,
        "evidence": "Asset down 20%, offsets gains in portfolio"
    }, headers=headers)
    assert exp_res.status_code == 200
    assert exp_res.json()["recommendation_id"] == "rec-999"
    
    # 3. Retrieve Explanation
    get_exp = client.get("/api/v1/foundation/explain/rec-999", headers=headers)
    assert get_exp.status_code == 200
    assert get_exp.json()["rule_applied"] == "Tax Loss Harvesting"
    
    # 4. Not Found Explanation
    not_found = client.get("/api/v1/foundation/explain/invalid-id", headers=headers)
    assert not_found.status_code == 404
