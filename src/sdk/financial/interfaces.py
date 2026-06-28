from typing import Protocol, List, Dict, Any

class IAccountService(Protocol):
    def get_account_balance(self, account_id: str) -> float:
        ...
        
    def list_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        ...

class ILedgerService(Protocol):
    def post_transaction(self, from_account: str, to_account: str, amount: float) -> str:
        ...

class ITransactionService(Protocol):
    def categorize_transaction(self, transaction_id: str, category: str) -> bool:
        ...
