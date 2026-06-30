from typing import Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class FeatureRegistered(DomainEvent):
    feature_id: str

class FeatureFlagCreated(DomainEvent):
    flag_id: str
    feature_id: str

class ExperimentStarted(DomainEvent):
    experiment_id: str

class ExperimentCompleted(DomainEvent):
    experiment_id: str
    winning_variant: str

class RolloutStarted(DomainEvent):
    rollout_id: str
    stage: str

class RolloutPaused(DomainEvent):
    rollout_id: str

class RolloutCompleted(DomainEvent):
    rollout_id: str

class RollbackTriggered(DomainEvent):
    feature_id: str
    reason: str

class FeatureEnabled(DomainEvent):
    feature_id: str

class FeatureDisabled(DomainEvent):
    feature_id: str

class TargetingRuleUpdated(DomainEvent):
    flag_id: str
