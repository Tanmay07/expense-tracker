from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class WealthProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    base_currency: str = "USD"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Portfolio(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    wealth_profile_id: str
    name: str  # e.g. "Retirement Portfolio", "Trading Account"
    broker: str
    currency: str = "USD"
    cash_balance: float = 0.0  # Internal uninvested cash
    status: str = "ACTIVE"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Holding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    portfolio_id: str
    asset_symbol: str  # e.g. AAPL, BTC, VOO
    asset_class: str  # EQUITY, CRYPTO, FIXED_INCOME
    quantity: float
    average_cost: float
    current_price: float = 0.0  # Updated by MarketDataSync
    currency: str = "USD"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def total_value(self) -> float:
        return self.quantity * self.current_price


class InvestmentTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    portfolio_id: str
    holding_id: Optional[str]
    transaction_type: str  # BUY, SELL, DIVIDEND, INTEREST, DEPOSIT, WITHDRAWAL
    asset_symbol: Optional[str]
    quantity: Optional[float]
    price_per_unit: Optional[float]
    total_amount: float
    fees: float = 0.0
    taxes: float = 0.0
    transaction_date: datetime = Field(default_factory=datetime.utcnow)
