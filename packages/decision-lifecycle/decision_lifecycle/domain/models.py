from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum

class LifecycleState(str, Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    ARCHIVED = "ARCHIVED"

class ObjectiveCategory(str, Enum):
    WEALTH_BUILDING = "WEALTH_BUILDING"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    LIQUIDITY = "LIQUIDITY"
    EFFICIENCY = "EFFICIENCY"

class Milestone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    completion_percentage: float = 0.0
    expected_date: Optional[datetime] = None
    actual_date: Optional[datetime] = None
    status: str = "PENDING"

class CheckpointStatus(str, Enum):
    ON_TRACK = "ON_TRACK"
    AHEAD = "AHEAD"
    BEHIND = "BEHIND"
    BLOCKED = "BLOCKED"
    NEEDS_REVISION = "NEEDS_REVISION"

class ExecutionStep(BaseModel):
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    is_automated: bool
    status: str = "PENDING"
    required_funds: float = 0.0

class RollbackPlan(BaseModel):
    triggers: List[str]
    steps: List[ExecutionStep]

class ExecutionPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    decision_id: str
    steps: List[ExecutionStep] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    rollback_plan: Optional[RollbackPlan] = None
    estimated_duration_days: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FinancialObjective(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    canonical_name: str
    category: ObjectiveCategory
    weight: float = 1.0
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
class DecisionLifecycle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    decision_id: str
    current_state: LifecycleState = LifecycleState.GENERATED
    state_history: List[Dict[str, Any]] = Field(default_factory=list)
    objective_id: Optional[str] = None
    execution_plan_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
