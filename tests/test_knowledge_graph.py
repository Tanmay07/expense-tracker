import pytest
from src.infrastructure.models import Transaction, Account
from src.knowledge_graph.database import MockGraphDatabase
from src.knowledge_graph.sync_service import GraphSyncService
from src.knowledge_graph.context_builder import RecommendationContextService
from datetime import datetime

def test_graph_sync_service_cypher_generation():
    db = MockGraphDatabase()
    sync_service = GraphSyncService(db)
    
    # Mock Data
    account = Account(id="acc_123", user_id="user_999", name="Checking")
    txn = Transaction(
        id="txn_456",
        user_id="user_999",
        account_id="acc_123",
        amount=50.0,
        transaction_type="EXPENSE",
        merchant="Starbucks",
        category="Coffee",
        transaction_date=datetime.utcnow()
    )
    
    # Run Sync
    sync_service.sync_transaction(txn, account)
    
    # Verify Cypher was sent to DB
    assert len(db.execution_log) == 1
    log = db.execution_log[0]
    
    assert "MERGE (u:User {id: $user_id})" in log["query"]
    assert "MERGE (m:Merchant {name: $merchant_name})" in log["query"]
    assert log["parameters"]["merchant_name"] == "Starbucks"
    assert log["parameters"]["amount"] == 50.0

def test_graph_context_builder():
    db = MockGraphDatabase()
    builder = RecommendationContextService(db)
    
    context = builder.build_user_context("user_999")
    
    # Expect our mock payload to be returned
    assert context["user_id"] == "user_999"
    assert "Frequent Traveler" in context["inferred_behaviors"]
    assert "Coffee" in context["spending_categories"]
    
    # Verify the traversal cypher was queried
    assert len(db.execution_log) == 1
    assert "MATCH (u:User {id: $user_id})" in db.execution_log[0]["query"]
