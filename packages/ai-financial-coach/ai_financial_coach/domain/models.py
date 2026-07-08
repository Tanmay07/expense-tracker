from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Role
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    explainability_metadata: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[Message] = Field(default_factory=list)
    context_summaries: List[str] = Field(default_factory=list)


class MemoryItemType(str, Enum):
    PREFERENCE = "PREFERENCE"
    FACT = "FACT"
    DECISION = "DECISION"
    BEHAVIOR = "BEHAVIOR"


class MemoryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: MemoryItemType
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expiration_date: Optional[datetime] = None
    confidence_score: float = 1.0


class PromptTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    template: str
    version: int = 1
    description: str
    tags: List[str] = Field(default_factory=list)


class AgentDefinition(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    system_prompt: str
    tools: List[str] = Field(default_factory=list)


class ActionProposal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    action_type: str
    parameters: Dict[str, Any]
    status: str = "PENDING_CONFIRMATION"  # PENDING_CONFIRMATION, ACCEPTED, REJECTED
    justification: str


class ContextFrame(BaseModel):
    metrics: Dict[str, Any] = Field(default_factory=dict)
    timeline_events: List[Dict[str, Any]] = Field(default_factory=list)
    graph_entities: List[Dict[str, Any]] = Field(default_factory=list)
    active_policies: List[Dict[str, Any]] = Field(default_factory=list)
    recent_memories: List[MemoryItem] = Field(default_factory=list)
