from typing import Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class StrategyPublished(DomainEvent):
    asset_id: str
    publisher_id: str
    categories: list[str]
    version: str

class StrategyDeprecated(DomainEvent):
    asset_id: str
    reason: str

class KnowledgeCapabilityAssigned(DomainEvent):
    asset_id: str
    scope: str
    visibility: str
    sensitivity: str
    ai_usability_json: Dict[str, Any]

class CertificationGranted(DomainEvent):
    asset_id: str
    certifier_id: str
    certification_tier: str

class CertificationRevoked(DomainEvent):
    asset_id: str
    reason: str

class MarketplaceAssetUpdated(DomainEvent):
    asset_id: str
    changed_fields: list[str]

class MarketplaceRankingUpdated(DomainEvent):
    asset_id: str
    new_overall_quality_score: float
    new_roi_score: float

class GovernanceApproved(DomainEvent):
    asset_id: str
    reviewer_id: str

class GovernanceRejected(DomainEvent):
    asset_id: str
    reviewer_id: str
    reason: str
