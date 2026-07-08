from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum


class AutomationLevel(str, Enum):
    MANUAL = "MANUAL"
    SEMI_AUTOMATED = "SEMI_AUTOMATED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    FULLY_AUTOMATED = "FULLY_AUTOMATED"
    SIMULATION_ONLY = "SIMULATION_ONLY"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExecutionPrerequisite(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # e.g., AUTHENTICATION, KYC, SUFFICIENT_BALANCE
    is_met: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)


class ExecutionCapability(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    automation_level: AutomationLevel
    risk_level: RiskLevel
    supported_platforms: List[str] = Field(default_factory=list)
    prerequisites: List[ExecutionPrerequisite] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class ApprovalRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    execution_step_id: str
    capability_id: str
    requested_by: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver_id: Optional[str] = None
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class ExecutionRoute(BaseModel):
    step_id: str
    selected_capability_id: str
    is_ready: bool = False
    pending_approvals: List[str] = Field(default_factory=list)
    unmet_prerequisites: List[str] = Field(default_factory=list)
