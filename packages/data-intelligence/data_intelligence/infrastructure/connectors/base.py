from typing import List, Dict, Any
from abc import ABC, abstractmethod
from data_intelligence.domain.events import FinancialEvent
import uuid
from datetime import datetime

class BaseConnector(ABC):
    @abstractmethod
    def sync(self, user_id: str) -> List[FinancialEvent]:
        pass

class GmailConnector(BaseConnector):
    def sync(self, user_id: str) -> List[FinancialEvent]:
        # Mocking an email parsing extraction
        return [
            FinancialEvent(
                event_id=str(uuid.uuid4()),
                user_id=user_id,
                source="GMAIL",
                connector_id="gmail_primary",
                raw_payload={"subject": "Your Uber ride", "body": "Total: $24.50"},
                transaction_date=datetime.utcnow(),
                amount=24.50,
                transaction_type="EXPENSE",
                merchant_raw="Uber BV",
                status="PENDING_REVIEW"
            )
        ]

class SMSConnector(BaseConnector):
    def sync(self, user_id: str) -> List[FinancialEvent]:
        # Mocking an SMS extraction
        return [
            FinancialEvent(
                event_id=str(uuid.uuid4()),
                user_id=user_id,
                source="SMS",
                connector_id="sms_android",
                raw_payload={"message": "Acct XX123 debited $5.00 at STARBUCKS"},
                transaction_date=datetime.utcnow(),
                amount=5.00,
                transaction_type="EXPENSE",
                merchant_raw="STARBUCKS",
                status="PENDING_REVIEW"
            )
        ]
