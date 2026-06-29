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

class DecisionGenerated(DomainEvent):
    event_type: str = "DecisionGenerated"

class DecisionOptimized(DomainEvent):
    event_type: str = "DecisionOptimized"

class DecisionScored(DomainEvent):
    event_type: str = "DecisionScored"

class ConstraintViolated(DomainEvent):
    event_type: str = "ConstraintViolated"

class DecisionBundled(DomainEvent):
    event_type: str = "DecisionBundled"

class OpportunityCostCalculated(DomainEvent):
    event_type: str = "OpportunityCostCalculated"

class EvidenceGenerated(DomainEvent):
    event_type: str = "EvidenceGenerated"
