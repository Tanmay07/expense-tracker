from typing import Dict, Any, List

class DashboardService:
    def __init__(self, account_service, transaction_service):
        self.account_service = account_service
        self.transaction_service = transaction_service
        
    def get_dashboard_summary(self, user_id: str) -> Dict[str, Any]:
        # Fetch all accounts to calculate Total Net Worth
        accounts = self.account_service.account_repo.list_for_user(user_id)
        total_balance = sum(acc.current_balance for acc in accounts)
        
        # Calculate Monthly Income / Expense
        # For Wave 1, we just sum up the existing transactions in memory
        income = 0.0
        expense = 0.0
        recent_txs = []
        
        # In a real DB, we'd query: SELECT sum(amount) WHERE user_id = ? AND type = 'INCOME'
        # Since TransactionRepository is likely a mock dictionary, we will just iterate it.
        user_txs = self.transaction_service.txn_repo.list_for_user(user_id)
        
        for tx in user_txs:
            if tx.transaction_type.name == "INCOME" or tx.transaction_type == "INCOME":
                income += tx.amount
            elif tx.transaction_type.name == "EXPENSE" or tx.transaction_type == "EXPENSE":
                expense += tx.amount
                
        # Sort and get recent 5
        sorted_txs = sorted(user_txs, key=lambda x: x.created_at, reverse=True)
        recent_txs = [{"id": tx.id, "amount": tx.amount, "type": tx.transaction_type.name if hasattr(tx.transaction_type, 'name') else tx.transaction_type, "merchant": tx.merchant} for tx in sorted_txs[:5]]

        return {
            "total_balance": total_balance,
            "monthly_income": income,
            "monthly_expense": expense,
            "savings": income - expense,
            "recent_transactions": recent_txs,
            "top_categories": [
                {"name": "Housing", "amount": expense * 0.4},
                {"name": "Food", "amount": expense * 0.2}
            ] # Mocked top categories for dashboard UI layout
        }
