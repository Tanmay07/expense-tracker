import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers():
    res = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.skip(reason="Pending package implementation")
def test_digital_twin_simulation():
    headers = get_auth_headers()
    
    # 1. Create a Scenario ("Buying a house in year 2")
    res1 = client.post("/api/v1/twin/scenarios", json={
        "name": "House Purchase",
        "events": [
            {"year": 2, "type": "EXPENSE", "amount": 100000.0}
        ]
    }, headers=headers)
    assert res1.status_code == 200
    scenario_id = res1.json()["scenario_id"]
    
    # 2. Run Monte Carlo Simulation (10 years, 100 iterations for speed)
    res2 = client.post(f"/api/v1/twin/simulate?scenario_id={scenario_id}&current_value=200000.0&years=10&iterations=100", headers=headers)
    assert res2.status_code == 200
    
    data = res2.json()
    assert data["years"] == 10
    assert "p50_expected" in data
    assert "p10_worst_case" in data
    assert "p90_best_case" in data
    
    # Since we subtract $100k in year 2, and start with 200k,
    # the expected portfolio shouldn't be astronomically high.
    # It should be roughly 100k * (1.05)^8 roughly. 
    assert data["p50_expected"] > 0
