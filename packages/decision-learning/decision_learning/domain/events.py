from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DecisionLearned(DomainEvent):
    decision_id: str
    user_id: str
    action_type: str
    execution_outcome: str

class PatternDetected(DomainEvent):
    user_id: str
    pattern_type: str
    confidence: float
    description: str

class RecommendationPersonalized(DomainEvent):
    user_id: str
    updated_fields: List[str]

class PolicyCacheUpdated(DomainEvent):
    decision_id: str
    policy_version: int
    is_valid: bool

class PredictionGenerated(DomainEvent):
    decision_id: str
    user_id: str
    acceptance_probability: float
    expected_roi: float

class FinancialDNAUpdated(DomainEvent):
    user_id: str
    changed_metrics: List[str]

class BehaviorChanged(DomainEvent):
    user_id: str
    evolution_type: str
    previous_value: Optional[str]
    new_value: Optional[str]

class LearningReplayGenerated(DomainEvent):
    session_id: str
