from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DecisionStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    WARNING = "WARNING"

class PolicyType(str, Enum):
    ALLOCATION = "ALLOCATION"
    RISK = "RISK"
    TAX = "TAX"
    LIQUIDITY = "LIQUIDITY"
    CURRENCY = "CURRENCY"
    BROKER = "BROKER"
    CUSTOM = "CUSTOM"

class PolicySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"

class RiskProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    risk_capacity: float
    risk_tolerance: float
    investment_horizon_years: int
    liquidity_needs: float
    income_stability_score: float
    emergency_fund_ratio: float
    overall_risk_level: RiskLevel
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CompliancePolicy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: PolicyType
    description: str
    severity: PolicySeverity
    rule_expression: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    jurisdiction: Optional[str] = None
    is_active: bool = True
    version: int = 1

class SuitabilityProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    suitability_score: float
    confidence_score: float
    last_evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    factors: Dict[str, Any] = Field(default_factory=dict)
    
class InvestmentConstraint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    constraint_type: str  # e.g., "ASSET_CLASS_LIMIT", "ESG_PREFERENCE"
    target: str          # e.g., "CRYPTO", "FOSSIL_FUELS"
    operator: str        # e.g., "MAX", "EXCLUDE"
    value: Any

class DecisionRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    context_id: str
    action_type: str     # e.g., "PORTFOLIO_REBALANCE", "RECOMMENDATION"
    status: DecisionStatus
    confidence: float
    policies_evaluated: List[str] = Field(default_factory=list)
    rules_triggered: List[str] = Field(default_factory=list)
    explanation: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    audit_trail: Dict[str, Any] = Field(default_factory=dict)
