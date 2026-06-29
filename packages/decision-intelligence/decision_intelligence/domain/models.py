from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum

class StrategyType(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    AGGRESSIVE = "AGGRESSIVE"
    LIQUIDITY_FIRST = "LIQUIDITY_FIRST"
    DEBT_FIRST = "DEBT_FIRST"
    RETIREMENT_FIRST = "RETIREMENT_FIRST"

class ConstraintViolation(BaseModel):
    constraint_name: str
    description: str
    severity: str

class ConfidenceScore(BaseModel):
    overall: float
    data_quality: float
    historical_accuracy: float
    model_confidence: float

class OpportunityCost(BaseModel):
    future_value: float
    goal_delay_months: int
    alternative_investment_yield: float
    explanation: str

class EvidenceGraph(BaseModel):
    knowledge_nodes: List[str]
    timeline_events: List[str]
    policies: List[str]
    simulations: List[str]

class SubScores(BaseModel):
    financial_impact: float
    risk: float
    urgency: float
    goal_alignment: float
    liquidity_impact: float

class DecisionCandidate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    strategy: StrategyType
    proposed_actions: List[Dict[str, Any]]
    
    overall_score: float = 0.0
    sub_scores: Optional[SubScores] = None
    
    opportunity_cost: Optional[OpportunityCost] = None
    confidence: Optional[ConfidenceScore] = None
    evidence: Optional[EvidenceGraph] = None
    
    constraint_violations: List[ConstraintViolation] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DecisionBundle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str # e.g., "Debt Bundle"
    candidates: List[DecisionCandidate]
    combined_score: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
