from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ContextPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ContextCardType(str, Enum):
    DEBT_ALERT = "DEBT_ALERT"
    EMERGENCY_FUND_PROGRESS = "EMERGENCY_FUND_PROGRESS"
    INVESTMENT_OPPORTUNITY = "INVESTMENT_OPPORTUNITY"
    SUBSCRIPTION_WASTE = "SUBSCRIPTION_WASTE"
    BILL_REMINDER = "BILL_REMINDER"
    SALARY_SUMMARY = "SALARY_SUMMARY"
    TAX_REMINDER = "TAX_REMINDER"
    PORTFOLIO_RISK = "PORTFOLIO_RISK"
    CASH_FLOW_FORECAST = "CASH_FLOW_FORECAST"
    INSURANCE_GAP = "INSURANCE_GAP"
    AI_RECOMMENDATION = "AI_RECOMMENDATION"


class AdaptiveAction(BaseModel):
    id: str
    label: str
    action_type: str
    icon: str
    payload: Dict[str, Any]
    primary: bool = False


class ContextExplanation(BaseModel):
    reason: str
    expected_impact: str
    recommended_action: str
    confidence_score: int
    supporting_evidence: List[str]


class ContextCard(BaseModel):
    id: str
    card_type: ContextCardType
    title: str
    description: str
    priority: ContextPriority
    explanation: ContextExplanation
    actions: List[AdaptiveAction]
    data: Dict[str, Any]


class FinancialContext(BaseModel):
    id: str
    name: str
    active: bool
    priority: ContextPriority
    confidence: int
    impact_score: int
    urgency: int
    recommended_mission_id: Optional[str]
    detected_at: datetime
    explanation: ContextExplanation
    cards: List[ContextCard]
