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


class PolicyCreated(DomainEvent):
    event_type: str = "PolicyCreated"


class PolicyEvaluated(DomainEvent):
    event_type: str = "PolicyEvaluated"


class ExecutionAuthorized(DomainEvent):
    event_type: str = "ExecutionAuthorized"


class ExecutionDenied(DomainEvent):
    event_type: str = "ExecutionDenied"


class PolicyConflictDetected(DomainEvent):
    event_type: str = "PolicyConflictDetected"
