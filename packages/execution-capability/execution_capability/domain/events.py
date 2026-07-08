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


class CapabilityRegistered(DomainEvent):
    event_type: str = "CapabilityRegistered"


class CapabilityUpdated(DomainEvent):
    event_type: str = "CapabilityUpdated"


class ExecutionRequested(DomainEvent):
    event_type: str = "ExecutionRequested"


class ApprovalRequested(DomainEvent):
    event_type: str = "ApprovalRequested"


class ApprovalGranted(DomainEvent):
    event_type: str = "ApprovalGranted"


class ExecutionFailed(DomainEvent):
    event_type: str = "ExecutionFailed"
