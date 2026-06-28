import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_finance_ledger_txns.db"
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

def test_transaction_expense_reduces_balance():
    # 1. Create Account with 1000 opening balance
    acc_payload = {
        "name": "Salary Account",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 1000.00,
        "is_primary": True,
        "user_id": "mock_user_123"
    }
    acc_resp = client.post("/api/v1/accounts", json=acc_payload)
    assert acc_resp.status_code == 201
    account_id = acc_resp.json()["id"]
    
    assert acc_resp.json()["current_balance"] == 1000.00
    
    # 2. Create Expense Transaction for 200
    txn_payload = {
        "account_id": account_id,
        "amount": 200.00,
        "transaction_type": "EXPENSE",
        "status": "CLEARED",
        "merchant": "Coffee Shop",
        "user_id": "mock_user_123"
    }
    txn_resp = client.post("/api/v1/transactions", json=txn_payload)
    assert txn_resp.status_code == 201
    
    # 3. Verify Account Balance is now 800
    acc_check = client.get(f"/api/v1/accounts/{account_id}")
    assert acc_check.json()["current_balance"] == 800.00
    
    # 4. Verify Ledger Entries (1 for opening, 1 for expense)
    ledger_resp = client.get(f"/api/v1/accounts/{account_id}/ledger")
    ledger_data = ledger_resp.json()
    assert len(ledger_data) == 2
    assert ledger_data[0]["amount"] == 200.00
    assert ledger_data[0]["entry_type"] == "DEBIT" # Newest first

def test_transaction_insufficient_funds_expense():
    # 1. Create Bank Account with 50 balance
    acc_payload = {
        "name": "Checking",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 50.00,
        "user_id": "mock_user_123"
    }
    acc_resp = client.post("/api/v1/accounts", json=acc_payload)
    account_id = acc_resp.json()["id"]
    
    # 2. Attempt Expense of 100
    txn_payload = {
        "account_id": account_id,
        "amount": 100.00,
        "transaction_type": "EXPENSE",
        "status": "CLEARED",
        "user_id": "mock_user_123"
    }
    txn_resp = client.post("/api/v1/transactions", json=txn_payload)
    assert txn_resp.status_code == 400
    assert "Insufficient funds" in txn_resp.json()["detail"]
