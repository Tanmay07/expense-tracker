from typing import Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class CanonicalTransaction(BaseModel):
    """
    The canonical PFOS representation of a financial transaction.
    All external connector data is mapped to this format before entering the Cognitive OS.
    """
    transaction_id: str
    connection_id: str
    user_id: str
    amount: float
    currency: str
    date: datetime
    description: str
    category: str = "uncategorized"
    merchant_name: str = "unknown"
    raw_data: Dict[str, Any] = Field(default_factory=dict)

class NormalizationEngine:
    """
    Transforms raw JSON payloads from specific external providers into Canonical models.
    """
    def __init__(self):
        # Maps connector types to their respective normalization logic
        self._schema_mappers = {
            "plaid": self._normalize_plaid,
            "stripe": self._normalize_stripe,
            "custom": self._normalize_custom
        }

    def normalize(self, provider_type: str, raw_payload: List[Dict[str, Any]], connection_id: str, user_id: str) -> List[CanonicalTransaction]:
        mapper = self._schema_mappers.get(provider_type, self._normalize_custom)
        return [mapper(record, connection_id, user_id) for record in raw_payload]

    def _normalize_plaid(self, record: Dict[str, Any], connection_id: str, user_id: str) -> CanonicalTransaction:
        return CanonicalTransaction(
            transaction_id=record.get("transaction_id", "unknown"),
            connection_id=connection_id,
            user_id=user_id,
            amount=float(record.get("amount", 0.0)),
            currency=record.get("iso_currency_code", "USD"),
            date=datetime.fromisoformat(record.get("date", datetime.now().isoformat())),
            description=record.get("name", "Unknown Transaction"),
            category=record.get("category", ["uncategorized"])[0],
            merchant_name=record.get("merchant_name", "unknown"),
            raw_data=record
        )

    def _normalize_stripe(self, record: Dict[str, Any], connection_id: str, user_id: str) -> CanonicalTransaction:
        # Stripe amounts are in cents
        amount = float(record.get("amount", 0)) / 100.0
        return CanonicalTransaction(
            transaction_id=record.get("id", "unknown"),
            connection_id=connection_id,
            user_id=user_id,
            amount=amount,
            currency=record.get("currency", "usd").upper(),
            date=datetime.fromtimestamp(record.get("created", datetime.now().timestamp())),
            description=record.get("description", "Stripe Charge"),
            merchant_name="Stripe Merchant",
            raw_data=record
        )

    def _normalize_custom(self, record: Dict[str, Any], connection_id: str, user_id: str) -> CanonicalTransaction:
        # Generic fallback
        return CanonicalTransaction(
            transaction_id=record.get("id", "unknown"),
            connection_id=connection_id,
            user_id=user_id,
            amount=float(record.get("amount", 0.0)),
            currency="USD",
            date=datetime.now(),
            description=str(record),
            raw_data=record
        )
