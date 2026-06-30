from typing import Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class ArchitectureValidated(DomainEvent):
    component_name: str
    is_compliant: bool

class WorkflowCertified(DomainEvent):
    workflow_id: str
    is_certified: bool

class PerformanceCertified(DomainEvent):
    endpoint: str
    is_certified: bool

class SecurityCertified(DomainEvent):
    component_name: str
    is_certified: bool

class ChaosExperimentCompleted(DomainEvent):
    scenario_name: str
    success: bool

class RecoveryValidated(DomainEvent):
    component_name: str
    success: bool

class MigrationValidated(DomainEvent):
    migration_id: str
    success: bool

class DocumentationCertified(DomainEvent):
    component_name: str
    score: float

class ReadinessCalculated(DomainEvent):
    version_tag: str
    score: float

class ProductionCertified(DomainEvent):
    version_tag: str

class ProductionCertificationFailed(DomainEvent):
    version_tag: str
    reason: str
