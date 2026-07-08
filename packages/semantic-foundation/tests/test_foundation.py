import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def get_auth_headers():
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.skip(reason="Pending package implementation")
def test_semantic_foundation_glossary_and_metadata():
    headers = get_auth_headers()

    # 1. Register a term in the Business Glossary
    res1 = client.post(
        "/api/v1/semantic/glossary",
        json={
            "term_id": "term_liquid_net_worth",
            "business_name": "Liquid Net Worth",
            "definition": "The total value of assets that can be rapidly converted to cash without significant loss of value.",
            "domain": "Wealth Management",
        },
        headers=headers,
    )
    assert res1.status_code == 200

    # 2. Tag the term with Metadata
    res2 = client.post(
        "/api/v1/semantic/metadata/tag",
        json={
            "concept_id": "term_liquid_net_worth",
            "tags": ["core_metric", "high_liquidity"],
            "documentation_url": "https://docs.finance-os.local/glossary/liquid_net_worth",
        },
        headers=headers,
    )
    assert res2.status_code == 200

    # 3. Retrieve the term and its metadata
    res3 = client.get(
        "/api/v1/semantic/glossary/term_liquid_net_worth", headers=headers
    )
    assert res3.status_code == 200
    assert res3.json()["business_name"] == "Liquid Net Worth"

    res4 = client.get(
        "/api/v1/semantic/metadata/term_liquid_net_worth", headers=headers
    )
    assert res4.status_code == 200
    assert "high_liquidity" in res4.json()["tags"]
