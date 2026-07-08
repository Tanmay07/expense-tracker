from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class PlatformBaseline(BaseModel):
    id: str
    version: str
    technical_metrics: Dict[str, float]
    business_metrics: Dict[str, float]
    ai_metrics: Dict[str, float]
    operational_metrics: Dict[str, float]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CertificationReport(BaseModel):
    id: str
    version: str
    architecture_certified: bool
    performance_certified: bool
    security_certified: bool
    governance_certified: bool
    operationally_ready: bool
    ai_certified: bool
    marketplace_certified: bool
    validation_certified: bool
    analytics_certified: bool
    mission_control_ready: bool
    overall_pass: bool
    risk_register: List[Dict[str, str]]
    technical_debt: List[Dict[str, str]]
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ContractVersionMatrix(BaseModel):
    version: str
    rest_apis: Dict[str, str]
    sdk_apis: Dict[str, str]
    events: Dict[str, str]
    plugins: Dict[str, str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DocumentationIndex(BaseModel):
    version: str
    documents: Dict[str, str]
    completeness_score: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GovernancePolicy(BaseModel):
    policy_id: str
    name: str
    description: str
    rules: List[str]
    enforced: bool

class ReleaseManifest(BaseModel):
    id: str
    version: str
    name: str = "PFOS Platform"
    certification_id: str
    baseline_id: str
    contract_matrix_id: str
    documentation_index_id: str
    release_notes: str
    breaking_changes: List[str]
    known_limitations: List[str]
    sbom: Dict[str, Any]
    architecture_hash: str
    platform_fingerprint: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
