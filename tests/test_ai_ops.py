import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_prompt_ab_testing():
    # User 1 should get a specific prompt
    res_1 = client.get("/api/v1/ops/prompts/active?template_name=financial_coach")
    assert res_1.status_code == 200
    p1 = res_1.json()["active_prompt"]
    assert "financial coach" in p1.lower() or "financial advisor" in p1.lower()

def test_drift_detection_normal():
    # Only 10% deviation, shouldn't drift
    res = client.post("/api/v1/ops/monitoring/check-drift?feature_name=avg_spend&current_val=55&baseline_val=50")
    assert res.status_code == 200
    assert res.json()["drift_detected"] is False

def test_drift_detection_drifting():
    # 100% deviation, should drift
    res = client.post("/api/v1/ops/monitoring/check-drift?feature_name=avg_spend&current_val=100&baseline_val=50")
    assert res.status_code == 200
    assert res.json()["drift_detected"] is True
    assert res.json()["action"] == "Trigger Retraining"
