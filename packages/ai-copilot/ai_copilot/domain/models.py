from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import uuid
from enum import Enum

class CopilotMode(str, Enum):
    DAILY_COACH = "DAILY_COACH"
    BUDGET_COACH = "BUDGET_COACH"
    INVESTMENT_COACH = "INVESTMENT_COACH"
    DEBT_COACH = "DEBT_COACH"
    GOAL_COACH = "GOAL_COACH"

class GoalConversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    goal_type: str # e.g., "Emergency Fund", "Retirement"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    active_mode: CopilotMode = CopilotMode.GOAL_COACH
    progress: float = 0.0
    action_history: List[str] = Field(default_factory=list)

class BehavioralProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    spending_behavior: str
    saving_habits: str
    investment_style: str
    risk_behavior: str
    financial_stress_indicators: List[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ActionStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    status: str = "PENDING"
    dependencies: List[str] = Field(default_factory=list)

class ActionPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    conversation_id: str
    priority: str
    expected_impact: str
    steps: List[ActionStep] = Field(default_factory=list)
    status: str = "PROPOSED"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SimulationRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    scenario_type: str # e.g. "Salary Change", "Market Crash"
    assumptions: Dict[str, Any]
    status: str = "PENDING"

class SimulationResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    outcomes: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float

class ProactiveAlert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    alert_type: str # e.g., "Budget Drift"
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False
