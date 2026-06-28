import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers():
    return {"Authorization": "Bearer password123"}

def test_financial_planning_engine():
    headers = get_auth_headers()
    
    # 1. Create a Budget
    res1 = client.post("/api/v1/planning/budgets", json={
        "name": "Groceries",
        "amount": 500.00,
        "period": "MONTHLY"
    }, headers=headers)
    assert res1.status_code == 200
    budget_id = res1.json()["id"]
    
    # 2. Spend against budget and exceed it
    res2 = client.post(f"/api/v1/planning/budgets/{budget_id}/spend?amount=600.00", headers=headers)
    assert res2.status_code == 200
    assert res2.json()["spent_amount"] == 600.00
    assert res2.json()["status"] == "EXCEEDED"
    
    # 3. Create a Goal
    res3 = client.post("/api/v1/planning/goals", json={
        "name": "Vacation Fund",
        "target_amount": 1000.00
    }, headers=headers)
    assert res3.status_code == 200
    goal_id = res3.json()["id"]
    
    # 4. Fund Goal
    res4 = client.post(f"/api/v1/planning/goals/{goal_id}/fund?amount=1000.00", headers=headers)
    assert res4.status_code == 200
    assert res4.json()["status"] == "ACHIEVED"

def test_financial_planning_step2():
    headers = get_auth_headers()
    
    # 1. Cashflow
    cf_res = client.get("/api/v1/planning/cashflow?days=30", headers=headers)
    assert cf_res.status_code == 200
    assert "net_cashflow" in cf_res.json()
    
    # 2. Forecast
    fc_res = client.get("/api/v1/planning/forecast?days_ahead=60", headers=headers)
    assert fc_res.status_code == 200
    assert "projected_balance" in fc_res.json()
    
    # 3. Health Score
    health_res = client.get("/api/v1/planning/health", headers=headers)
    assert health_res.status_code == 200
    assert health_res.json()["overall_score"] == 75
    
    # 4. Recommendations
    rec_res = client.get("/api/v1/planning/recommendations", headers=headers)
    assert rec_res.status_code == 200
    assert len(rec_res.json()) > 0
    assert rec_res.json()[0]["action_type"] in ["REDUCE_SPENDING", "INCREASE_SAVINGS"]

def test_financial_planning_step3():
    headers = get_auth_headers()
    
    # 1. Subscriptions
    sub_res = client.post("/api/v1/planning/subscriptions", json={
        "name": "Netflix",
        "cost": 15.99,
        "billing_cycle": "MONTHLY",
        "next_billing_date": "2026-07-01T00:00:00Z"
    }, headers=headers)
    assert sub_res.status_code == 200
    assert sub_res.json()["status"] == "ACTIVE"
    
    # 2. Bills
    bill_res = client.post("/api/v1/planning/bills", json={
        "biller_name": "Electric Co",
        "amount": 120.50,
        "due_date": "2026-07-15T00:00:00Z"
    }, headers=headers)
    assert bill_res.status_code == 200
    bill_id = bill_res.json()["id"]
    
    # 3. Pay Bill
    pay_res = client.post(f"/api/v1/planning/bills/{bill_id}/pay", headers=headers)
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "PAID"
    
    # 4. Recurring Tx
    req_res = client.post("/api/v1/planning/recurring", json={
        "name": "Salary",
        "amount": 5000.00,
        "transaction_type": "INCOME",
        "rrule": "FREQ=MONTHLY;BYMONTHDAY=1"
    }, headers=headers)
    assert req_res.status_code == 200
    assert req_res.json()["rrule"] == "FREQ=MONTHLY;BYMONTHDAY=1"
