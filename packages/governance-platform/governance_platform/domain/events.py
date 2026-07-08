from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class GovernanceCreated(DomainEvent):
    policy_id: str
    name: str

class GovernanceApproved(DomainEvent):
    asset_id: str
    workflow_id: str

class TrustUpdated(DomainEvent):
    asset_id: str
    new_score: float
    is_trusted: bool

class EvidenceRecorded(DomainEvent):
    ledger_id: str
    asset_id: str
    evidence_type: str

class CertificationGranted(DomainEvent):
    asset_id: str
    certification_level: str

class CertificationRevoked(DomainEvent):
    asset_id: str
    reason: str

class PolicyEvaluated(DomainEvent):
    asset_id: str
    policy_id: str
    is_compliant: bool

class AssuranceCompleted(DomainEvent):
    asset_id: str

class GovernanceViolationDetected(DomainEvent):
    asset_id: str
    violation_type: str
    details: str
