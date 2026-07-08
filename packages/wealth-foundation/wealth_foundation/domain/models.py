from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class Household(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # e.g. "Smith Family"
    base_currency: str = "USD"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FamilyMember(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    household_id: str
    user_id: Optional[str] = None  # Optional for minors/dependents
    name: str
    role: str  # PRIMARY, SPOUSE, CHILD, DEPENDENT, GUARDIAN
    ownership_percentage: float = 100.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Currency(BaseModel):
    code: str  # e.g., USD, EUR, INR
    name: str
    symbol: str


class FXRate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    base_currency: str
    target_currency: str
    rate: float
    provider: str = "MOCK_PROVIDER"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CorporateAction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_symbol: str
    action_type: str  # SPLIT, DIVIDEND, MERGER
    ratio: Optional[float] = None  # e.g. 2.0 for 2-for-1 split
    amount_per_share: Optional[float] = None
    execution_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "PENDING"  # PENDING, APPLIED


class GoalFunding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal_id: str
    asset_id: str  # e.g. Holding ID or Portfolio ID
    allocation_percentage: float = (
        100.0  # Percentage of the asset dedicated to this goal
    )
    priority: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProviderPlugin(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # e.g. PLAID, YODLEE, YAHOO_FINANCE
    provider_type: str  # MARKET_DATA, BROKER, FX, TAX
    is_active: bool = True
    priority: int = 1
    capabilities: List[str] = []  # e.g. ["REALTIME_QUOTES", "HISTORICAL_PRICES"]


class WealthExplanation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recommendation_id: str
    rule_applied: str
    confidence_score: float
    evidence: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Custodian(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # e.g. "JPMorgan", "Fidelity", "Binance"
    custodian_type: str  # BANK, BROKER, MUTUAL_FUND, CRYPTO
    is_active: bool = True
    capabilities: List[str] = []  # e.g. ["ASSET_SYNC", "TRADE_EXECUTION"]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Broker(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    custodian_id: str
    name: str  # e.g. "Fidelity Retail"
    auth_mechanism: str  # OAUTH, API_KEY
    status: str = "ACTIVE"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AssetCustody(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str  # The abstract holding ID
    broker_id: str  # Where it is physically held
    quantity: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TaxLot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    broker_id: str
    quantity: float
    unit_price: float
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "OPEN"  # OPEN, CLOSED
    lot_type: str = "FIFO"


class WealthPolicy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    household_id: str
    name: str  # e.g. "Maximum Equity Allocation 80%"
    policy_type: str  # ALLOCATION, RISK, RESTRICTION
    parameters: dict = {}  # e.g. {"max_equity": 0.8}
    is_active: bool = True


class PortfolioPolicy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    portfolio_id: str
    name: str  # e.g. "No Crypto"
    policy_type: str  # COMPLIANCE, TAX
    parameters: dict = {}
    is_active: bool = True


class HouseholdPermission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    household_id: str
    user_id: str
    role: str  # OWNER, ADVISOR, READ_ONLY, AUDITOR
    granted_by: str
    granted_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class WealthSnapshot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str  # household_id or portfolio_id
    entity_type: str  # HOUSEHOLD, PORTFOLIO
    snapshot_date: datetime
    net_worth: float
    asset_allocation: dict = {}
    metrics: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReplayState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    target_date: datetime
    entity_id: str
    entity_type: str
    state_data: dict = {}
    replayed_at: datetime = Field(default_factory=datetime.utcnow)
