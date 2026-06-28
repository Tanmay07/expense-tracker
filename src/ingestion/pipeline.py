from typing import List, Dict, Any
from datetime import datetime
from src.domain.schemas import TransactionCreate
from src.domain.enums import TransactionType

class NormalizationService:
    @staticmethod
    def normalize_amount(raw_amount: str) -> float:
        if not raw_amount: return 0.0
        # Remove commas, currency symbols, handle negatives
        clean = str(raw_amount).replace(",", "").replace("$", "").replace("₹", "").strip()
        try:
            return float(clean)
        except ValueError:
            return 0.0

    @staticmethod
    def normalize_date(raw_date: str) -> datetime:
        if not raw_date: return datetime.utcnow()
        # Very simple normalizer for proof-of-concept
        # Real system would use dateutil.parser
        formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"]
        for f in formats:
            try:
                return datetime.strptime(raw_date.strip(), f)
            except ValueError:
                continue
        return datetime.utcnow()

class IngestionPipeline:
    def __init__(self, connector: 'BaseConnector', account_id: str, user_id: str):
        self.connector = connector
        self.account_id = account_id
        self.user_id = user_id
        
    def process(self, storage_path: str) -> List[TransactionCreate]:
        raw_records = self.connector.extract(storage_path)
        valid_transactions = []
        
        for record in raw_records:
            # 1. Normalize
            amount = NormalizationService.normalize_amount(record.get("amount"))
            date = NormalizationService.normalize_date(record.get("transaction_date"))
            merchant = record.get("merchant", "Unknown")
            
            # Determine type
            txn_type = TransactionType.INCOME if amount > 0 else TransactionType.EXPENSE
            amount = abs(amount)
            
            # 2. Map to DTO
            txn = TransactionCreate(
                account_id=self.account_id,
                amount=amount,
                transaction_type=txn_type,
                merchant=merchant,
                user_id=self.user_id,
                status="CLEARED", # Assuming imported cleared
                source="CSV"
            )
            
            # 3. Validation (Skipped for brevity, relies on schemas)
            
            valid_transactions.append(txn)
            
        return valid_transactions
