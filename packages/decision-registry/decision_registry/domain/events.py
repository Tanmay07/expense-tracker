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


class DecisionCreated(DomainEvent):
    event_type: str = "DecisionCreated"


class DecisionUpdated(DomainEvent):
    event_type: str = "DecisionUpdated"


class DecisionArchived(DomainEvent):
    event_type: str = "DecisionArchived"


class DecisionVersionCreated(DomainEvent):
    event_type: str = "DecisionVersionCreated"


class DecisionRelationshipAdded(DomainEvent):
    event_type: str = "DecisionRelationshipAdded"


class DecisionProvenanceUpdated(DomainEvent):
    event_type: str = "DecisionProvenanceUpdated"


class DecisionRestored(DomainEvent):
    event_type: str = "DecisionRestored"


class DecisionDeleted(DomainEvent):
    event_type: str = "DecisionDeleted"
