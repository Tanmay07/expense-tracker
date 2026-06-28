import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_agent_permissions_denied():
    # Budget Agent shouldn't be allowed to execute transfers
    res = client.post("/api/v1/agents/execute?agent_role=budget_agent&intent=transfer+500")
    assert res.status_code == 200
    assert res.json()["status"] == "failed"
    assert "Permission denied" in res.json()["reason"]

def test_agent_human_in_the_loop_pause():
    # Wealth Agent is allowed, but transfer requires HIGH security HITL checkpoint
    res = client.post("/api/v1/agents/execute?agent_role=wealth_agent&intent=transfer+500")
    assert res.status_code == 200
    assert res.json()["status"] == "paused"
    assert res.json()["pending_tool"] == "execute_transfer"
    
    execution_id = res.json()["execution_id"]
    
    # Now simulate human approval
    res_approve = client.post(f"/api/v1/agents/approve?execution_id={execution_id}")
    assert res_approve.status_code == 200
    assert res_approve.json()["status"] == "resumed"

def test_agent_simple_read():
    # Simple read doesn't require pausing
    res = client.post("/api/v1/agents/execute?agent_role=budget_agent&intent=check+my+balance")
    assert res.status_code == 200
    assert res.json()["status"] == "completed"
    assert "query_ledger" in res.json()["executed_tools"]
