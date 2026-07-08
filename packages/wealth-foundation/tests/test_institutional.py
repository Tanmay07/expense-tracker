# pyrefly: ignore [missing-import]
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def get_auth_headers():
    return {"Authorization": "Bearer password123"}


@pytest.mark.skip(reason="Pending package implementation")
def test_wealth_institutional_step1():
    headers = get_auth_headers()

    # 1. Register Custodian
    cust_res = client.post(
        "/api/v1/foundation/custodians",
        json={
            "name": "JPMorgan Chase",
            "custodian_type": "BANK",
            "capabilities": ["ASSET_SYNC"],
        },
        headers=headers,
    )
    assert cust_res.status_code == 200
    custodian_id = cust_res.json()["id"]
    assert cust_res.json()["name"] == "JPMorgan Chase"

    # 2. Link Broker
    broker_res = client.post(
        "/api/v1/foundation/brokers",
        json={
            "custodian_id": custodian_id,
            "name": "JPM Retail",
            "auth_mechanism": "OAUTH",
        },
        headers=headers,
    )
    assert broker_res.status_code == 200
    broker_id = broker_res.json()["id"]

    # 3. Assign Asset Custody
    custody_res = client.post(
        f"/api/v1/foundation/brokers/{broker_id}/custody",
        json={"asset_id": "holding-nvda-123", "quantity": 50.0},
        headers=headers,
    )
    assert custody_res.status_code == 200
    assert custody_res.json()["asset_id"] == "holding-nvda-123"
    assert custody_res.json()["quantity"] == 50.0

    # 4. Invalid Broker
    bad_custody = client.post(
        "/api/v1/foundation/brokers/invalid-broker/custody",
        json={"asset_id": "holding-nvda-123", "quantity": 50.0},
        headers=headers,
    )
    assert bad_custody.status_code == 400


@pytest.mark.skip(reason="Pending package implementation")
def test_wealth_institutional_step2():
    headers = get_auth_headers()

    # 1. Generate Tax Lot
    lot_res = client.post(
        "/api/v1/foundation/tax-lots",
        json={
            "asset_id": "holding-nvda-123",
            "broker_id": "broker-fidelity-456",
            "quantity": 10.0,
            "unit_price": 125.50,
        },
        headers=headers,
    )
    assert lot_res.status_code == 200
    assert lot_res.json()["quantity"] == 10.0
    assert lot_res.json()["unit_price"] == 125.50
    assert lot_res.json()["status"] == "OPEN"

    # 2. Create Wealth Policy
    wp_res = client.post(
        "/api/v1/foundation/policies/wealth",
        json={
            "household_id": "hh-789",
            "name": "Max Equity 80%",
            "policy_type": "ALLOCATION",
            "parameters": {"max_equity": 0.8},
        },
        headers=headers,
    )
    assert wp_res.status_code == 200
    assert wp_res.json()["policy_type"] == "ALLOCATION"
    assert wp_res.json()["parameters"]["max_equity"] == 0.8

    # 3. Create Portfolio Policy
    pp_res = client.post(
        "/api/v1/foundation/policies/portfolio",
        json={
            "portfolio_id": "port-999",
            "name": "No Crypto Allowed",
            "policy_type": "RESTRICTION",
            "parameters": {"forbidden_assets": ["BTC", "ETH"]},
        },
        headers=headers,
    )
    assert pp_res.status_code == 200
    assert pp_res.json()["policy_type"] == "RESTRICTION"
    assert "BTC" in pp_res.json()["parameters"]["forbidden_assets"]


@pytest.mark.skip(reason="Pending package implementation")
def test_wealth_institutional_step3():
    headers = get_auth_headers()

    # 1. Grant Permission
    perm_res = client.post(
        "/api/v1/foundation/permissions",
        json={
            "household_id": "hh-789",
            "user_id": "user-advisor-1",
            "role": "ADVISOR",
            "granted_by": "user-owner-1",
        },
        headers=headers,
    )
    assert perm_res.status_code == 200
    assert perm_res.json()["role"] == "ADVISOR"
    assert perm_res.json()["is_active"] is True

    # 2. Generate Snapshot
    snap_res = client.post(
        "/api/v1/foundation/snapshots",
        json={
            "entity_id": "hh-789",
            "entity_type": "HOUSEHOLD",
            "snapshot_date": "2026-06-01T00:00:00Z",
            "net_worth": 1500000.50,
            "asset_allocation": {"EQUITY": 0.7, "FIXED_INCOME": 0.3},
        },
        headers=headers,
    )
    assert snap_res.status_code == 200
    assert snap_res.json()["net_worth"] == 1500000.50
    assert snap_res.json()["asset_allocation"]["EQUITY"] == 0.7

    # 3. Build Replay State
    replay_res = client.post(
        "/api/v1/foundation/replay",
        json={
            "entity_id": "hh-789",
            "entity_type": "HOUSEHOLD",
            "target_date": "2025-12-31T00:00:00Z",
            "state_data": {"net_worth": 1200000.00, "positions": 15},
        },
        headers=headers,
    )
    assert replay_res.status_code == 200
    assert replay_res.json()["state_data"]["net_worth"] == 1200000.00
