import pytest
from trust_platform.domain.models import ConsentStatus


@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "trust-platform"}


@pytest.mark.asyncio
async def test_record_consent(client, mock_db_session):
    payload = {
        "user_id": "user_123",
        "purpose": "MARKETING",
        "status": ConsentStatus.GRANTED.value,
    }
    response = client.post("/api/v1/trust/consent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["purpose"] == "MARKETING"
    assert data["status"] == "GRANTED"


@pytest.mark.asyncio
async def test_log_ai_execution(client, mock_db_session):
    payload = {
        "capability_used": "BudgetOptimizer",
        "reasoning_summary": "Optimized budget to save 10%",
        "confidence": 0.95,
        "safety_checks": {"no_pii": True},
        "bias_evaluation": {"score": 0.0},
    }
    response = client.post("/api/v1/trust/ai", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["capability_used"] == "BudgetOptimizer"
    assert data["confidence"] == 0.95
    assert "id" in data


@pytest.mark.asyncio
async def test_evaluate_risk(client, mock_db_session):
    payload = {"target_id": "transaction_789", "category": "FINANCIAL", "score": 85.5}
    response = client.post("/api/v1/trust/risk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "FINANCIAL"
    assert data["score"] == 85.5


@pytest.mark.asyncio
async def test_append_audit_log(client, mock_db_session):
    payload = {
        "event_type": "ACCESS_GRANTED",
        "actor_id": "admin_01",
        "action": "GRANTED_READ_ACCESS",
        "target_id": "document_999",
        "metadata": {"ip_address": "192.168.1.1"},
    }
    response = client.post("/api/v1/trust/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "ACCESS_GRANTED"
    assert data["actor_id"] == "admin_01"
    assert data["is_immutable"] is True


@pytest.mark.asyncio
async def test_calculate_trust_score(client, mock_db_session):
    payload = {
        "entity_id": "user_123",
        "entity_type": "USER",
        "score": 98.0,
        "factors": {"identity_verified": 100.0, "past_behavior": 96.0},
    }
    response = client.post("/api/v1/trust/scores", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 98.0
    assert data["entity_id"] == "user_123"
