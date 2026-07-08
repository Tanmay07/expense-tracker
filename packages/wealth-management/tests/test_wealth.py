import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def get_auth_headers():
    return {"Authorization": "Bearer password123"}


@pytest.mark.skip(reason="Pending package implementation")
def test_wealth_management_step1():
    headers = get_auth_headers()

    # 1. Create Portfolio
    p_res = client.post(
        "/api/v1/wealth/portfolios",
        json={"name": "Vanguard Retirement", "broker": "Vanguard"},
        headers=headers,
    )
    assert p_res.status_code == 200
    portfolio_id = p_res.json()["id"]

    # 2. Deposit Cash
    dep_res = client.post(
        f"/api/v1/wealth/portfolios/{portfolio_id}/deposit?amount=10000.00",
        headers=headers,
    )
    assert dep_res.status_code == 200
    assert dep_res.json()["cash_balance"] == 10000.00

    # 3. Buy Investment (Apple Stock)
    buy_res = client.post(
        "/api/v1/wealth/investments/buy",
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "AAPL",
            "asset_class": "EQUITY",
            "quantity": 10.0,
            "price": 150.0,
        },
        headers=headers,
    )
    assert buy_res.status_code == 200
    assert buy_res.json()["total_amount"] == 1500.0

    # 4. Try to buy exceeding cash balance (should fail)
    bad_buy = client.post(
        "/api/v1/wealth/investments/buy",
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "TSLA",
            "asset_class": "EQUITY",
            "quantity": 100.0,
            "price": 200.0,  # 20k cost, only 8500 left
        },
        headers=headers,
    )
    assert bad_buy.status_code == 400
