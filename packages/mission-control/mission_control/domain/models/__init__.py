from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum


class MissionType(str, Enum):
    TODAYS_TASKS = "TODAYS_TASKS"
    CRITICAL_ALERTS = "CRITICAL_ALERTS"
    FINANCIAL_WINS = "FINANCIAL_WINS"
    RECOMMENDED_ACTIONS = "RECOMMENDED_ACTIONS"
    UPCOMING_BILLS = "UPCOMING_BILLS"
    INVESTMENT_OPPORTUNITIES = "INVESTMENT_OPPORTUNITIES"
    SAVINGS_SUGGESTIONS = "SAVINGS_SUGGESTIONS"
    BUDGET_ADJUSTMENTS = "BUDGET_ADJUSTMENTS"
    GOAL_MILESTONES = "GOAL_MILESTONES"


class MissionStatus(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    COMPLETED = "COMPLETED"
    DISMISSED = "DISMISSED"
    EXPIRED = "EXPIRED"
    DEFERRED = "DEFERRED"
    ESCALATED = "ESCALATED"


class MissionPriority(BaseModel):
    level: str = "LOW"  # HIGH, MEDIUM, LOW, CRITICAL
    urgency_score: float
    financial_impact_score: float
    confidence: float
    business_impact: str


class MissionExplanation(BaseModel):
    summary: str
    supporting_metrics: Dict[str, Any]
    timeline_events: List[str]
    policies_evaluated: List[str]
    simulation_results: Optional[Dict[str, Any]] = None
    expected_financial_benefit: float


class ActionTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    requires_confirmation: bool = True
    action_payload: Dict[str, Any]


class Mission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    type: MissionType
    status: MissionStatus = MissionStatus.CREATED
    priority: MissionPriority
    explanation: MissionExplanation
    actions: List[ActionTask] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Opportunity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: str
    score: float
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Risk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
