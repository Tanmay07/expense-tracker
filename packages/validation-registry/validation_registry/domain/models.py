from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ArtifactRecord(BaseModel):
    id: str
    canonical_name: str
    description: Optional[str] = None
    category: str
    producer: str
    pipeline_id: Optional[str] = None
    sandbox_run_id: Optional[str] = None
    strategy_id: Optional[str] = None
    version: str = "1.0.0"
    status: str = "ACTIVE"
    owner_id: str
    tags: List[str] = Field(default_factory=list)
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

    storage_location: str
    checksum_sha256: str
    digital_signature: Optional[str] = None
    is_encrypted: bool = False
    is_compressed: bool = False
    integrity_status: str = "VERIFIED"

    created_at: datetime
    expires_at: Optional[datetime] = None
    retention_policy: str = "30_DAYS"

    model_config = ConfigDict(from_attributes=True)


class ArtifactRecordCreate(BaseModel):
    canonical_name: str
    description: Optional[str] = None
    category: str
    producer: str
    pipeline_id: Optional[str] = None
    sandbox_run_id: Optional[str] = None
    strategy_id: Optional[str] = None
    version: str = "1.0.0"
    owner_id: str
    tags: List[str] = Field(default_factory=list)
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    retention_policy: str = "30_DAYS"


class ArtifactLineage(BaseModel):
    id: str
    source_id: str
    target_id: str
    relationship_type: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class EvidencePackage(BaseModel):
    id: str
    package_name: str
    artifact_ids: List[str]
    certification_id: Optional[str] = None
    compliance_framework: Optional[str] = None
    digital_signature: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ReuseEvaluation(BaseModel):
    id: str
    target_artifact_id: str
    input_hash: str
    policy_version: Optional[str] = None
    model_version: Optional[str] = None
    is_reusable: bool
    confidence_score: float
    reason: Optional[str] = None
    evaluated_at: datetime
    model_config = ConfigDict(from_attributes=True)
