from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# --- Enums ---


class MemberRole(str, Enum):
    OWNER = "OWNER"
    CO_OWNER = "CO_OWNER"
    DEPENDENT = "DEPENDENT"
    ADVISOR = "ADVISOR"
    VIEWER = "VIEWER"


class DelegationScope(str, Enum):
    VIEW_ONLY = "VIEW_ONLY"
    COMMENT = "COMMENT"
    RECOMMEND = "RECOMMEND"
    MANAGE_BUDGETS = "MANAGE_BUDGETS"
    EXECUTE_ACTIONS = "EXECUTE_ACTIONS"
    FULL_ADMIN = "FULL_ADMIN"


class MissionStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# --- Models ---


class Household(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    settings: Dict[str, Any] = Field(default_factory=dict)


class HouseholdMember(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    household_id: str
    user_id: str
    role: MemberRole
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class Advisor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    firm_name: Optional[str] = None
    specialty: str
    certification_details: Dict[str, Any] = Field(default_factory=dict)


class Delegation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    delegator_user_id: str
    delegatee_user_id: str
    scope: DelegationScope
    household_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class SharedWorkspace(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    household_id: Optional[str] = None
    owner_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SharedMission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workspace_id: str
    title: str
    description: str
    status: MissionStatus = MissionStatus.PROPOSED
    owners: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    thread_id: str
    sender_id: str
    content: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    read_by: List[str] = Field(default_factory=list)


class HouseholdPolicy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    household_id: str
    policy_type: str  # e.g., "SPENDING_LIMIT", "APPROVAL_REQUIRED"
    rules: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
