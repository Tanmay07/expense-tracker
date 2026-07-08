from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class FinancialEvent(BaseModel):
    """
    Canonical Financial Event representing unstructured data successfully parsed and normalized.
    This acts as a buffer before hitting the Core Ledger.
    """

    event_id: str
    user_id: str

    # Provenance
    source: str  # GMAIL, SMS, OCR, PDF, MANUAL
    connector_id: str
    raw_payload: Dict[str, Any]

    # Extracted Data
    transaction_date: datetime
    amount: float
    currency: str = "USD"
    transaction_type: str  # INCOME, EXPENSE, TRANSFER

    # Intelligence
    merchant_raw: str
    merchant_normalized: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    # Confidence & State
    ai_confidence: float = 0.0
    status: str = "PENDING_REVIEW"  # PENDING_REVIEW, VERIFIED, REJECTED, DUPLICATE

    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
