from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class DomainEvent(BaseModel):
    event_id: str
    timestamp: datetime = datetime.utcnow()
    event_type: str

class PlatformCertified(DomainEvent):
    event_type: str = "PlatformCertified"
    version: str
    overall_pass: bool
    certification_id: str

class PlatformReleased(DomainEvent):
    event_type: str = "PlatformReleased"
    version: str
    manifest_id: str

class ArchitectureFrozen(DomainEvent):
    event_type: str = "ArchitectureFrozen"
    version: str
    architecture_hash: str

class ContractsFrozen(DomainEvent):
    event_type: str = "ContractsFrozen"
    version: str
    contract_matrix_id: str

class BaselineCaptured(DomainEvent):
    event_type: str = "BaselineCaptured"
    version: str
    baseline_id: str

class DocumentationFrozen(DomainEvent):
    event_type: str = "DocumentationFrozen"
    version: str
    completeness_score: float

class MissionControlCertified(DomainEvent):
    event_type: str = "MissionControlCertified"
    version: str

class PlatformVersionPublished(DomainEvent):
    event_type: str = "PlatformVersionPublished"
    version: str
