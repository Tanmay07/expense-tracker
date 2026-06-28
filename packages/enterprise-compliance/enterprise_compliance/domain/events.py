from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    event_type: str
    payload: Dict[str, Any]

class SuitabilityEvaluated(DomainEvent):
    event_type: str = "SuitabilityEvaluated"

class ComplianceChecked(DomainEvent):
    event_type: str = "ComplianceChecked"

class PolicyApplied(DomainEvent):
    event_type: str = "PolicyApplied"

class PolicyViolated(DomainEvent):
    event_type: str = "PolicyViolated"

class RiskProfileUpdated(DomainEvent):
    event_type: str = "RiskProfileUpdated"

class DecisionGoverned(DomainEvent):
    event_type: str = "DecisionGoverned"

class RecommendationValidated(DomainEvent):
    event_type: str = "RecommendationValidated"

class RegulationUpdated(DomainEvent):
    event_type: str = "RegulationUpdated"

class ConstraintChanged(DomainEvent):
    event_type: str = "ConstraintChanged"

class AuditRecorded(DomainEvent):
    event_type: str = "AuditRecorded"
