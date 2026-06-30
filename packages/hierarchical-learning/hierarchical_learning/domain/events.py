from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class LearningObserved(DomainEvent):
    scope: str # GLOBAL, REGIONAL, HOUSEHOLD, PERSONAL
    topic: str
    entity_id: str
    knowledge_json: Dict[str, Any]

class KnowledgePromoted(DomainEvent):
    promotion_id: str
    source_scope: str
    target_scope: str
    topic: str
    new_status: str

class KnowledgeValidated(DomainEvent):
    promotion_id: str
    confidence_score: float
    is_valid: bool

class KnowledgePublished(DomainEvent):
    target_scope: str
    entity_id: str
    topic: str
    published_knowledge: Dict[str, Any]

class KnowledgeDeprecated(DomainEvent):
    scope: str
    entity_id: str
    topic: str
    reason: str

class BehaviorUpdated(DomainEvent):
    user_id: str
    topic: str
    new_embedding: Optional[list[float]] = None

class ConsensusReached(DomainEvent):
    consensus_id: str
    household_id: str
    topic: str
    resolved_consensus: Dict[str, Any]

class PrivacyPolicyChanged(DomainEvent):
    user_id: str
    opted_out_topics: list[str]

class LearningDecayed(DomainEvent):
    scope: str
    entity_id: str
    topic: str
    decay_amount: float
    new_confidence: float
