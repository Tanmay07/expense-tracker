from src.knowledge_graph.database import BaseGraphDatabase
from src.infrastructure.models import Transaction, Account
from typing import List

class GraphSyncService:
    """
    Consumes Domain Events (or direct calls) and syncs the PostgreSQL 
    truth into the Neo4j/Apache AGE Graph schema using MERGE statements for idempotency.
    """
    def __init__(self, db: BaseGraphDatabase):
        self.db = db

    def sync_transaction(self, txn: Transaction, account: Account):
        """
        Translates a Transaction into a Graph neighborhood:
        (User)-[:OWNS]->(Account)
        (Account)-[:HAS_TRANSACTION]->(Transaction)
        (Transaction)-[:OCCURRED_AT]->(Merchant)
        (Transaction)-[:BELONGS_TO]->(Category)
        """
        merchant_name = txn.merchant if txn.merchant else "Unknown"
        category_name = txn.category if txn.category else "Uncategorized"
        
        cypher = """
        MERGE (u:User {id: $user_id})
        MERGE (a:Account {id: $account_id})
        MERGE (u)-[:OWNS]->(a)
        
        MERGE (t:Transaction {id: $txn_id})
        SET t.amount = $amount, t.date = $date, t.type = $type
        MERGE (a)-[:HAS_TRANSACTION]->(t)
        
        MERGE (m:Merchant {name: $merchant_name})
        MERGE (t)-[:OCCURRED_AT]->(m)
        
        MERGE (c:Category {name: $category_name})
        MERGE (t)-[:BELONGS_TO]->(c)
        MERGE (m)-[:CATEGORIZED_AS]->(c)
        """
        
        params = {
            "user_id": txn.user_id,
            "account_id": account.id,
            "txn_id": txn.id,
            "amount": txn.amount,
            "date": str(txn.transaction_date),
            "type": txn.transaction_type,
            "merchant_name": merchant_name,
            "category_name": category_name
        }
        
        self.db.execute_cypher(cypher, params)
