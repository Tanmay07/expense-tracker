from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class GovernancePolicy(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    domain: str
    version: str = "1.0.0"
    policy_payload_json: Dict[str, Any]
    status: str = "DRAFT"
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class GovernancePolicyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    domain: str
    version: str = "1.0.0"
    policy_payload_json: Dict[str, Any]

class TrustScore(BaseModel):
    id: str
    asset_id: str
    validation_score: float = 0.0
    lineage_score: float = 0.0
    ai_confidence_score: float = 0.0
    policy_compliance_score: float = 0.0
    marketplace_usage_score: float = 0.0
    composite_trust_score: float = 0.0
    is_trusted: bool = False
    last_calculated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MaturityRecord(BaseModel):
    id: str
    asset_id: str
    current_level: str
    promoted_at: datetime
    promoted_by: str
    reason: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AIGovernanceRecord(BaseModel):
    id: str
    asset_id: str
    hallucination_rate: float = 0.0
    bias_score: float = 0.0
    fairness_score: float = 0.0
    prompt_drift: float = 0.0
    privacy_violation_count: float = 0.0
    evaluated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AIGovernanceRecordCreate(BaseModel):
    asset_id: str
    hallucination_rate: float = 0.0
    bias_score: float = 0.0
    fairness_score: float = 0.0
    prompt_drift: float = 0.0
    privacy_violation_count: float = 0.0

class EvidenceLedgerEntry(BaseModel):
    id: str
    asset_id: str
    evidence_type: str
    payload_hash: str
    digital_signature: str
    signer_id: str
    previous_ledger_id: Optional[str] = None
    recorded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WorkflowState(BaseModel):
    id: str
    asset_id: str
    workflow_type: str
    current_state: str
    assigned_reviewer_id: Optional[str] = None
    comments: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
