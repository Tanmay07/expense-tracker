from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUEST_CLARIFICATION = "REQUEST_CLARIFICATION"
    SCHEDULED = "SCHEDULED"


class ApprovalLevel(str, Enum):
    INFORM_ONLY = "INFORM_ONLY"
    RECOMMENDATION = "RECOMMENDATION"
    ONE_CLICK = "ONE_CLICK"
    TWO_STEP = "TWO_STEP"
    HOUSEHOLD = "HOUSEHOLD"


class ApprovalMetadata(BaseModel):
    title: str
    summary: str
    reason: str
    expected_financial_impact: Optional[str] = None
    expected_risks: List[str] = Field(default_factory=list)
    confidence_score: float
    alternative_options: List[str] = Field(default_factory=list)
    estimated_cost: Optional[str] = None
    estimated_benefit: Optional[str] = None
    undo_availability: bool = False
    rollback_availability: bool = False
    referenced_policies: List[str] = Field(default_factory=list)


class ToolInvocation(BaseModel):
    id: str
    tool_name: str
    arguments: Dict[str, Any]
    status: str = "PENDING"
    result: Optional[Dict[str, Any]] = None
    requires_approval: bool = False
    approval_level: Optional[ApprovalLevel] = None
    approval_metadata: Optional[ApprovalMetadata] = None
    approval_status: Optional[ApprovalStatus] = None
    error: Optional[str] = None


class AITurn(BaseModel):
    id: str
    role: Role
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_invocations: List[ToolInvocation] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolConfig(BaseModel):
    name: str
    description: str
    schema_definition: Dict[str, Any]
    requires_approval: bool = False
    feature_flag: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)


class AIContextMetadata(BaseModel):
    active_workspace: Optional[str] = None
    selected_entity_id: Optional[str] = None
    active_mission: Optional[str] = None
    current_time: datetime = Field(default_factory=datetime.utcnow)
    user_persona: Optional[str] = None


class ConversationSession(BaseModel):
    id: str
    title: str
    turns: List[AITurn] = Field(default_factory=list)
    context_snapshot: AIContextMetadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AICapability(BaseModel):
    id: str
    name: str
    description: str
    version: str
    category: str
    supported_input_types: List[str] = Field(default_factory=list)
    supported_output_types: List[str] = Field(default_factory=list)
    streaming_support: bool = False
    multimodal_support: bool = False
    requires_approval: bool = False
    expected_latency: str = "low"
    offline_availability: bool = False
    feature_flag: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)
