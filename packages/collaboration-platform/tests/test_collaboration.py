import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "collaboration-platform"}

@pytest.mark.asyncio
async def test_create_household(client, mock_db_session):
    # Mock the database execute/add operations if necessary
    # Assuming the repository handles adding without deep ORM magic in the test
    payload = {
        "name": "Smith Family",
        "owner_id": "user_123"
    }
    response = client.post("/api/v1/collaboration/households", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Smith Family"
    assert "id" in data

@pytest.mark.asyncio
async def test_register_advisor(client, mock_db_session):
    payload = {
        "user_id": "advisor_456",
        "specialty": "Tax Planning",
        "firm_name": "Wealth Management LLC"
    }
    response = client.post("/api/v1/collaboration/advisors", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["specialty"] == "Tax Planning"
    assert data["firm_name"] == "Wealth Management LLC"

@pytest.mark.asyncio
async def test_create_delegation(client, mock_db_session):
    payload = {
        "delegator_user_id": "user_123",
        "delegatee_user_id": "advisor_456",
        "scope": "VIEW_ONLY",
        "household_id": "hh_789"
    }
    response = client.post("/api/v1/collaboration/delegations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scope"] == "VIEW_ONLY"
    assert data["delegator_user_id"] == "user_123"
    assert data["delegatee_user_id"] == "advisor_456"

@pytest.mark.asyncio
async def test_create_shared_space(client, mock_db_session):
    payload = {
        "name": "Estate Planning",
        "owner_id": "user_123",
        "household_id": "hh_789"
    }
    response = client.post("/api/v1/collaboration/shared-spaces", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Estate Planning"
    assert data["owner_id"] == "user_123"
