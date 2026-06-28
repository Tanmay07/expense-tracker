import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_finance_ledger_recon.db"
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

@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    yield db
    db.close()

def test_net_worth_calculation():
    # 1. Create a Bank Account (Asset)
    acc1_payload = {
        "name": "Checking Asset",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 5000.00,
        "is_primary": True,
        "user_id": "mock_user_123"
    }
    client.post("/api/v1/accounts", json=acc1_payload)

    # 2. Create a Credit Card (Liability)
    acc2_payload = {
        "name": "Credit Card Liability",
        "account_type": "CREDIT_CARD",
        "currency_code": "USD",
        "opening_balance": -1000.00,
        "is_primary": False,
        "user_id": "mock_user_123"
    }
    client.post("/api/v1/accounts", json=acc2_payload)
    
    # 3. Calculate Net Worth
    # Since opening balances are zeroed by our repository and properly added via ledger, we can calculate it
    # But wait, did we post a transaction or just open? The ledger service processes opening balance internally.
    nw_resp = client.get("/api/v1/balances/net-worth")
    assert nw_resp.status_code == 200
    data = nw_resp.json()
    assert data["total_assets"] >= 5000.00
    assert data["total_liabilities"] >= 1000.00
    assert data["net_worth"] == data["total_assets"] - data["total_liabilities"]

def test_recalculation_service(test_db):
    # 1. Create an Account
    acc_payload = {
        "name": "Checking to drift",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 0.0,
        "user_id": "mock_user_999"
    }
    acc_resp = client.post("/api/v1/accounts", json=acc_payload)
    account_id = acc_resp.json()["id"]

    # 2. Add an Income transaction of $1000
    txn_payload = {
        "account_id": account_id,
        "amount": 1000.00,
        "transaction_type": "INCOME",
        "status": "CLEARED",
        "user_id": "mock_user_999"
    }
    client.post("/api/v1/transactions", json=txn_payload)
    
    acc_check = client.get(f"/api/v1/accounts/{account_id}")
    assert acc_check.json()["current_balance"] == 1000.0
    
    # 3. Force a drift (simulate a concurrent write issue or bug)
    from src.infrastructure.models import Account
    acc = test_db.query(Account).filter(Account.id == account_id).first()
    acc.current_balance = 500.0 # Incorrectly set to 500
    test_db.commit()
    
    acc_check2 = client.get(f"/api/v1/accounts/{account_id}")
    assert acc_check2.json()["current_balance"] == 500.0
    
    # 4. Run Recalculation
    recalc_resp = client.post(f"/api/v1/accounts/{account_id}/recalculate")
    assert recalc_resp.status_code == 200
    assert recalc_resp.json()["new_balance"] == 1000.0
    
    # 5. Check if Account is fixed
    acc_check3 = client.get(f"/api/v1/accounts/{account_id}")
    assert acc_check3.json()["current_balance"] == 1000.0
