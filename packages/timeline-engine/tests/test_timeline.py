import pytest
from fastapi.testclient import TestClient
from src.main import app
import time

client = TestClient(app)

def get_auth_headers():
    res = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

def test_timeline_event_sourcing_and_replay():
    headers = get_auth_headers()
    
    t1 = time.time()
    
    # 1. Salary Credit (+$5000)
    res1 = client.post("/api/v1/timeline/events", json={
        "event_type": "LEDGER_CREDIT",
        "payload": {"amount": 5000.0, "description": "Salary"},
        "timestamp": t1
    }, headers=headers)
    assert res1.status_code == 200
    
    # 2. Rent Paid (-$1500)
    t2 = t1 + 100
    res2 = client.post("/api/v1/timeline/events", json={
        "event_type": "LEDGER_DEBIT",
        "payload": {"amount": 1500.0, "description": "Rent"},
        "timestamp": t2
    }, headers=headers)
    assert res2.status_code == 200
    
    # 3. Asset Appreciates (+$500)
    t3 = t2 + 100
    res3 = client.post("/api/v1/timeline/events", json={
        "event_type": "ASSET_APPRECIATION",
        "payload": {"amount": 500.0, "description": "AAPL gain"},
        "timestamp": t3
    }, headers=headers)
    assert res3.status_code == 200
    
    # --- Time Travel Tests ---
    
    # Replay exactly at t1 (Should be $5000)
    rep1 = client.get(f"/api/v1/timeline/replay/net_worth?target_timestamp={t1}", headers=headers)
    assert rep1.status_code == 200
    assert rep1.json()["reconstructed_net_worth"] == 5000.0
    
    # Replay exactly at t2 (Should be 5000 - 1500 = 3500)
    rep2 = client.get(f"/api/v1/timeline/replay/net_worth?target_timestamp={t2}", headers=headers)
    assert rep2.json()["reconstructed_net_worth"] == 3500.0
    
    # Replay at t3 (Should be 3500 + 500 = 4000)
    rep3 = client.get(f"/api/v1/timeline/replay/net_worth?target_timestamp={t3}", headers=headers)
    assert rep3.json()["reconstructed_net_worth"] == 4000.0
