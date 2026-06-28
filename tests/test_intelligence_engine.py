import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_categorization_pipeline():
    # 1. Test User Rule Match
    res_1 = client.post("/api/v1/intelligence/categorize?merchant=Landlord+LLC&amount=1000")
    assert res_1.status_code == 200
    assert res_1.json()["source"] == "USER_RULE"
    assert res_1.json()["category"] == "Housing"
    
    # 2. Test ML Match (High Confidence)
    res_2 = client.post("/api/v1/intelligence/categorize?merchant=Amazon&amount=50")
    assert res_2.status_code == 200
    assert res_2.json()["source"] == "ML_CLASSIFIER"
    
    # 3. Test LLM Fallback (Low Confidence ML)
    res_3 = client.post("/api/v1/intelligence/categorize?merchant=Obscure+Store&amount=25")
    assert res_3.status_code == 200
    assert res_3.json()["source"] == "LLM_SEMANTIC_FALLBACK"

def test_anomaly_detection():
    # 1. Normal Transaction (close to avg 45.50)
    res_1 = client.post("/api/v1/intelligence/anomaly-score?amount=50")
    assert res_1.status_code == 200
    assert res_1.json()["is_anomaly"] is False
    
    # 2. Anomalous Transaction (10x average)
    res_2 = client.post("/api/v1/intelligence/anomaly-score?amount=5000")
    assert res_2.status_code == 200
    assert res_2.json()["is_anomaly"] is True
