import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_wave1_registration_and_dashboard():
    # 1. Register a new user
    res1 = client.post("/api/v1/auth/register", json={
        "email": "wave1@example.com",
        "password": "securepassword123"
    })
    assert res1.status_code == 200
    user_id = res1.json()["user_id"]
    
    # 2. Login to get JWT
    res2 = client.post("/api/v1/auth/login", data={
        "username": "wave1@example.com",
        "password": "securepassword123"
    })
    assert res2.status_code == 200
    token = res2.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create an Account
    res3 = client.post("/api/v1/accounts", json={
        "name": "Checking",
        "account_type": "BANK",
        "currency_code": "USD",
        "user_id": "mocked_by_endpoint"
    }, headers=headers)
    print(res3.json())
    assert res3.status_code == 201
    
    # 4. Fetch the Dashboard
    res4 = client.get("/api/v1/dashboard/summary", headers=headers)
    assert res4.status_code == 200
    data = res4.json()
    assert "total_balance" in data
    assert "monthly_income" in data
    assert "savings" in data
    assert type(data["recent_transactions"]) == list
