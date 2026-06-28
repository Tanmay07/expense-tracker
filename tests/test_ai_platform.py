import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_ai_execution_and_semantic_cache():
    # 1. First request (Cache Miss)
    payload_1 = {
        "query": "How can I reduce my expenses?",
        "template_id": "SYS_BUDGET_REVIEW_V1"
    }
    
    response_1 = client.post("/api/v1/ai/execute", json=payload_1)
    assert response_1.status_code == 200
    data_1 = response_1.json()["response"]
    
    # It should hit the mock LLM
    assert "[MOCK_LLM_RESPONSE via openai]" in data_1
    assert "[CACHE HIT]" not in data_1
    
    # 2. Exact same request (Cache Hit)
    response_2 = client.post("/api/v1/ai/execute", json=payload_1)
    assert response_2.status_code == 200
    data_2 = response_2.json()["response"]
    
    # It should hit the Semantic Cache bypassing the LLM
    assert "[CACHE HIT]" in data_2
    assert "[MOCK_LLM_RESPONSE via openai]" in data_2
