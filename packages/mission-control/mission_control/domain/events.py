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

class MissionGenerated(DomainEvent):
    event_type: str = "MissionGenerated"

class MissionUpdated(DomainEvent):
    event_type: str = "MissionUpdated"

class MissionCompleted(DomainEvent):
    event_type: str = "MissionCompleted"

class MissionDismissed(DomainEvent):
    event_type: str = "MissionDismissed"

class RiskDetected(DomainEvent):
    event_type: str = "RiskDetected"

class OpportunityDetected(DomainEvent):
    event_type: str = "OpportunityDetected"

class ActionExecuted(DomainEvent):
    event_type: str = "ActionExecuted"
