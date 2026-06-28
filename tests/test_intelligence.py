import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.models import ClassificationRule, Merchant, MerchantAlias, Category
from src.domain.enums import RuleType, RuleCondition, RuleAction

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_finance_ledger_intel.db"
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

def test_merchant_normalization_and_classification(test_db):
    # Setup data
    cat = Category(name="Coffee", category_type="BUILTIN")
    test_db.add(cat)
    
    merch = Merchant(name="Starbucks")
    test_db.add(merch)
    test_db.commit()
    test_db.refresh(merch)
    test_db.refresh(cat)
    
    alias = MerchantAlias(merchant_id=merch.id, alias="Star Bucks")
    rule = ClassificationRule(
        user_id="mock_user_123",
        rule_type=RuleType.MERCHANT,
        condition_field="merchant",
        condition_operator=RuleCondition.EQUALS,
        condition_value="Starbucks", # Note this is the canonical name
        action_type=RuleAction.SET_CATEGORY,
        action_value="Coffee" # Setting string for legacy compatibility in this test
    )
    test_db.add(alias)
    test_db.add(rule)
    test_db.commit()

    # Create account
    acc_payload = {
        "name": "Checking",
        "account_type": "BANK",
        "currency_code": "USD",
        "opening_balance": 1000.00,
        "is_primary": True,
        "user_id": "mock_user_123"
    }
    acc_resp = client.post("/api/v1/accounts", json=acc_payload)
    account_id = acc_resp.json()["id"]

    # Transaction with un-normalized alias
    txn_payload = {
        "account_id": account_id,
        "amount": 5.00,
        "transaction_type": "EXPENSE",
        "merchant": "Star Bucks", # Alias!
        "user_id": "mock_user_123"
    }
    
    txn_resp = client.post("/api/v1/transactions", json=txn_payload)
    assert txn_resp.status_code == 201
    
    data = txn_resp.json()
    assert data["merchant"] == "Starbucks" # Must be normalized!
    assert data["category"] == "Coffee"    # Must be categorized via rule!
    
def test_fuzzy_matching():
    from src.application.services import SearchService
    choices = ["Starbucks", "Amazon", "Netflix", "Spotify"]
    
    assert SearchService.fuzzy_match_merchant("Starbuks", choices) == "Starbucks"
    assert SearchService.fuzzy_match_merchant("Amzon", choices) == "Amazon"
    assert SearchService.fuzzy_match_merchant("Netflx", choices) == "Netflix"
    assert SearchService.fuzzy_match_merchant("RandomString", choices) == None
