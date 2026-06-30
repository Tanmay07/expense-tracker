from typing import Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class ArtifactCreated(DomainEvent):
    artifact_id: str
    canonical_name: str
    category: str
    owner_id: str

class ArtifactVersionCreated(DomainEvent):
    artifact_id: str
    canonical_name: str
    new_version: str

class ArtifactIndexed(DomainEvent):
    artifact_id: str
    storage_location: str

class ArtifactArchived(DomainEvent):
    artifact_id: str

class ArtifactExpired(DomainEvent):
    artifact_id: str

class ArtifactRestored(DomainEvent):
    artifact_id: str
    restored_by: str

class ArtifactVerified(DomainEvent):
    artifact_id: str
    checksum_sha256: str
    status: str

class EvidencePackageCreated(DomainEvent):
    package_id: str
    package_name: str
    artifact_count: int

class ReuseSuggested(DomainEvent):
    target_artifact_id: str
    input_hash: str
    confidence_score: float

class LineageUpdated(DomainEvent):
    source_id: str
    target_id: str
    relationship_type: str

class IntegrityViolationDetected(DomainEvent):
    artifact_id: str
    expected_checksum: str
    actual_checksum: str
