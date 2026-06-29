from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    event_type: str
    payload: Dict[str, Any]

class DecisionStateChanged(DomainEvent):
    event_type: str = "DecisionStateChanged"

class ObjectiveCreated(DomainEvent):
    event_type: str = "ObjectiveCreated"

class ExecutionPlanCreated(DomainEvent):
    event_type: str = "ExecutionPlanCreated"

class MilestoneReached(DomainEvent):
    event_type: str = "MilestoneReached"

class RollbackTriggered(DomainEvent):
    event_type: str = "RollbackTriggered"

class CheckpointEvaluated(DomainEvent):
    event_type: str = "CheckpointEvaluated"
