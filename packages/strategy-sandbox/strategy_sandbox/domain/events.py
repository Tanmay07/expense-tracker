from typing import Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class ValidationStarted(DomainEvent):
    run_id: str
    asset_id: str
    profile_id: str

class ValidationCompleted(DomainEvent):
    run_id: str
    asset_id: str
    status: str
    composite_score: float

class ValidationFailed(DomainEvent):
    run_id: str
    asset_id: str
    failed_stage: str
    reason: str

class BenchmarkCompleted(DomainEvent):
    run_id: str
    benchmark_type: str

class FitnessCalculated(DomainEvent):
    run_id: str
    composite_score: float

class PromptValidated(DomainEvent):
    run_id: str
    hallucination_score: float
    policy_compliance_score: float

class CertificationGranted(DomainEvent):
    run_id: str
    asset_id: str
    certification_level: str

class CertificationRevoked(DomainEvent):
    asset_id: str
    reason: str

class StrategyPublishedReady(DomainEvent):
    asset_id: str
    certification_level: str
