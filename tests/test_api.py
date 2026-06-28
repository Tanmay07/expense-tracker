import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_finance_ledger.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "finance-os-ledger"}

def test_create_account():
    payload = {
        "name": "My Checking Account",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 1500.00,
        "is_primary": True,
        "user_id": "mock_user_123"
    }
    response = client.post("/api/v1/accounts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Checking Account"
    assert data["current_balance"] == 1500.00
    
    account_id = data["id"]
    
    # Check ledger entries for opening balance
    ledger_resp = client.get(f"/api/v1/accounts/{account_id}/ledger")
    assert ledger_resp.status_code == 200
    ledger_data = ledger_resp.json()
    assert len(ledger_data) == 1
    assert ledger_data[0]["amount"] == 1500.00
    assert ledger_data[0]["entry_type"] == "CREDIT"

def test_negative_opening_balance_for_bank_fails():
    payload = {
        "name": "Checking Account Negative",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": -100.00,
        "user_id": "mock_user_123"
    }
    response = client.post("/api/v1/accounts", json=payload)
    assert response.status_code == 400

def test_negative_opening_balance_for_credit_card_succeeds():
    payload = {
        "name": "Credit Card",
        "account_type": "CREDIT_CARD",
        "currency_code": "USD",
        "opening_balance": -500.00,
        "user_id": "mock_user_123"
    }
    response = client.post("/api/v1/accounts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["current_balance"] == -500.00
