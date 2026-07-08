import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.skip(reason="Pending package implementation")
def test_control_plane_discovery():
    # 1. Register an OCR Plugin
    res1 = client.post("/api/v1/control/register?service_name=ocr-plugin&endpoint=http://ocr:8000&capabilities=EXTRACT_RECEIPT,PARSE_PDF")
    assert res1.status_code == 200
    assert res1.json()["status"] == "registered"
    
    # 2. Agent Requests Capability
    res2 = client.get("/api/v1/control/discover?capability=EXTRACT_RECEIPT")
    assert res2.status_code == 200
    assert res2.json()["status"] == "found"
    assert res2.json()["service"]["endpoint"] == "http://ocr:8000"
    
    # 3. Request unknown capability
    res3 = client.get("/api/v1/control/discover?capability=QUANTUM_COMPUTE")
    assert res3.status_code == 200
    assert res3.json()["status"] == "not_found"

@pytest.mark.skip(reason="Pending package implementation")
def test_control_plane_config():
    # 1. Retrieve feature flag
    res1 = client.get("/api/v1/control/config/enable_ai_agent")
    assert res1.status_code == 200
    assert res1.json()["value"] is True
    
    # 2. Retrieve config
    res2 = client.get("/api/v1/control/config/max_tokens_per_user")
    assert res2.status_code == 200
    assert res2.json()["value"] == "5000"
