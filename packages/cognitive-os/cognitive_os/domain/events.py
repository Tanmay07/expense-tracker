from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any


class DomainEvent(BaseModel):
    event_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    event_type: str
    payload: Dict[str, Any]


class MissionCreated(DomainEvent):
    event_type: str = "MissionCreated"


class ConsensusReached(DomainEvent):
    event_type: str = "ConsensusReached"


class ReflectionCompleted(DomainEvent):
    event_type: str = "ReflectionCompleted"
