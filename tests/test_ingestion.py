import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import io
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_finance_ledger_ingest.db"
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

def test_csv_import_pipeline():
    # 1. Create a Bank Account
    acc_payload = {
        "name": "Checking Pipeline",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 1000.00,
        "user_id": "mock_user_123"
    }
    acc_resp = client.post("/api/v1/accounts", json=acc_payload)
    account_id = acc_resp.json()["id"]
    
    # 2. Mock a CSV File upload
    csv_content = """Date,Desc,Amt
2026-06-25,Starbucks Coffee,5.50
2026-06-26,Salary Corp,3000.00
2026-06-27,Amazon,-150.75"""

    # Map the custom headers to our system schemas
    mapping = {
        "Date": "transaction_date",
        "Desc": "merchant",
        "Amt": "amount"
    }
    
    # Upload File (fastapi format)
    response = client.post(
        "/api/v1/import/csv",
        data={
            "account_id": account_id,
            "mapping": json.dumps(mapping)
        },
        files={
            "file": ("statement.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
        }
    )
    
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["processed"] == 3
    assert res_data["status"] == "completed"
    
    # Verify balance
    acc_check = client.get(f"/api/v1/accounts/{account_id}")
    # Opening 1000 + 3000 (Income) - 5.50 (Expense) - 150.75 (Expense) = 3843.75
    # Wait, the CSV amount parsing handles negatives.
    # The normalizer makes amount absolute and deduces type from +/-
    # So "3000.00" -> INCOME
    # "-150.75" -> EXPENSE
    # "5.50" -> INCOME (wait! if positive is income in this CSV layout, then Starbucks was income. Let's see.)
    # In my tests "5.50" > 0 so it's INCOME, "-150.75" is EXPENSE.
    # 1000 + 5.5 + 3000 - 150.75 = 3854.75
    assert acc_check.json()["current_balance"] == 3854.75
