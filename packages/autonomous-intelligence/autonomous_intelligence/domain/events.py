import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class BaseDomainEvent(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"


class AgentRegistered(BaseDomainEvent):
    agent_id: uuid.UUID
    name: str
    role: str


class MissionCreated(BaseDomainEvent):
    mission_id: uuid.UUID
    agent_id: uuid.UUID
    goal_id: Optional[uuid.UUID] = None


class MissionCompleted(BaseDomainEvent):
    mission_id: uuid.UUID
    agent_id: uuid.UUID
    status: str
    outcomes: Dict[str, Any] = Field(default_factory=dict)


class GoalUpdated(BaseDomainEvent):
    goal_id: uuid.UUID
    agent_id: uuid.UUID
    status: str
    current_amount: Optional[float] = None


class PlanGenerated(BaseDomainEvent):
    plan_id: uuid.UUID
    agent_id: uuid.UUID
    horizon: str


class ApprovalRequested(BaseDomainEvent):
    mission_id: uuid.UUID
    agent_id: uuid.UUID
    action_type: str
    details: Dict[str, Any]


class AgentCollaborated(BaseDomainEvent):
    source_agent_id: uuid.UUID
    target_agent_id: uuid.UUID
    collaboration_type: str  # DELEGATION, NEGOTIATION, CONSENSUS


class EvaluationCompleted(BaseDomainEvent):
    evaluation_id: uuid.UUID
    agent_id: uuid.UUID
    trust_score: float
    goal_completion_score: float
