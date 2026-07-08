from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# --- Enums ---


class ConsentStatus(str, Enum):
    GRANTED = "GRANTED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"


class RiskCategory(str, Enum):
    FINANCIAL = "FINANCIAL"
    SECURITY = "SECURITY"
    OPERATIONAL = "OPERATIONAL"
    PRIVACY = "PRIVACY"
    COMPLIANCE = "COMPLIANCE"
    AI = "AI"


class PrivacyRequestType(str, Enum):
    ACCESS = "ACCESS"
    RECTIFICATION = "RECTIFICATION"
    ERASURE = "ERASURE"
    PORTABILITY = "PORTABILITY"
    RESTRICT_PROCESSING = "RESTRICT_PROCESSING"


# --- Models ---


class TrustPolicy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    rules: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TrustScore(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str
    entity_type: str  # e.g., USER, CONNECTOR, ADVISOR
    score: float  # 0.0 to 100.0
    factors: Dict[str, float] = Field(default_factory=dict)
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


class ConsentRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    purpose: str
    status: ConsentStatus
    version: int = 1
    granted_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class PrivacyRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    request_type: PrivacyRequestType
    status: str = "PENDING"
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ComplianceProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # e.g., "GDPR", "SOC2"
    version: str
    controls: List[Dict[str, Any]] = Field(default_factory=list)


class AITrustRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    capability_used: str
    reasoning_summary: str
    confidence: float
    safety_checks: Dict[str, bool] = Field(default_factory=dict)
    bias_evaluation: Dict[str, Any] = Field(default_factory=dict)
    approval_required: bool = False
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    # chain_of_thought is deliberately excluded for privacy/security


class RiskScore(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    target_id: str
    category: RiskCategory
    score: float  # 0.0 (low) to 100.0 (high)
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    actor_id: str
    target_id: Optional[str] = None
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_immutable: bool = True
