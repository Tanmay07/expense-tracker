import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.mark.skip(reason="Pending package implementation")
def test_governance_scorecard():
    res = client.post(
        "/api/v1/governance/evaluate?package_name=ledger&has_tests=true&has_adr=true"
    )
    assert res.status_code == 200
    assert res.json()["score"] == 100
    assert res.json()["status"] == "Enterprise Ready"


@pytest.mark.skip(reason="Pending package implementation")
def test_governance_policy_ast_import():
    import urllib.parse

    bad_file = "from sqlalchemy import create_engine\nengine = create_engine()"
    encoded = urllib.parse.quote(bad_file)
    res = client.post(f"/api/v1/governance/validate-imports?file_content={encoded}")
    assert res.status_code == 200
    assert res.json()["status"] == "failed"


@pytest.mark.skip(reason="Pending package implementation")
def test_finops_aggregation():
    # Post AI token cost
    res1 = client.post(
        "/api/v1/finops/record?resource_type=gpt4_tokens&units=1000&unit_price=0.03"
    )
    assert res1.status_code == 200

    res2 = client.get("/api/v1/finops/dashboard")
    assert res2.status_code == 200
    assert res2.json()["gpt4_tokens"] >= 30.0
