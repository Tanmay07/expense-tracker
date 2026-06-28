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

class ConversationStarted(DomainEvent):
    event_type: str = "ConversationStarted"

class MemoryUpdated(DomainEvent):
    event_type: str = "MemoryUpdated"

class DecisionGenerated(DomainEvent):
    event_type: str = "DecisionGenerated"

class RecommendationAccepted(DomainEvent):
    event_type: str = "RecommendationAccepted"

class RecommendationRejected(DomainEvent):
    event_type: str = "RecommendationRejected"

class ContextBuilt(DomainEvent):
    event_type: str = "ContextBuilt"

class GraphRetrieved(DomainEvent):
    event_type: str = "GraphRetrieved"
