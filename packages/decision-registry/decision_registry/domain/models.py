from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum


class DecisionType(str, Enum):
    RECOMMENDATION = "RECOMMENDATION"
    AUTOMATION = "AUTOMATION"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"


class DecisionCategory(str, Enum):
    INVESTMENT = "INVESTMENT"
    BUDGET = "BUDGET"
    DEBT = "DEBT"
    TAX = "TAX"
    INSURANCE = "INSURANCE"


class DecisionStatus(str, Enum):
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    ARCHIVED = "ARCHIVED"


class DecisionScope(str, Enum):
    PORTFOLIO = "PORTFOLIO"
    ACCOUNT = "ACCOUNT"
    GOAL = "GOAL"
    GLOBAL = "GLOBAL"


class DecisionPriority(BaseModel):
    level: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    importance_score: float


class DecisionMetadata(BaseModel):
    source: str
    owner: str
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    summary: str
    narrative: str
    context: Dict[str, Any] = Field(default_factory=dict)
    attachments: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)


class DecisionProvenance(BaseModel):
    metrics_used: List[str] = Field(default_factory=list)
    policies_used: List[str] = Field(default_factory=list)
    knowledge_graph_snapshot_id: Optional[str] = None
    timeline_snapshot_id: Optional[str] = None
    digital_twin_snapshot_id: Optional[str] = None
    prompt_version: Optional[str] = None
    model_version: Optional[str] = None
    sdk_versions: Dict[str, str] = Field(default_factory=dict)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    connector_ids: List[str] = Field(default_factory=list)
    user_feedback_references: List[str] = Field(default_factory=list)
    simulation_references: List[str] = Field(default_factory=list)
    learning_hooks: Dict[str, Any] = Field(default_factory=dict)


class DecisionRelationshipType(str, Enum):
    DEPENDS_ON = "DEPENDS_ON"
    SUPPORTS_GOAL = "SUPPORTS_GOAL"
    AFFECTS_BUDGET = "AFFECTS_BUDGET"
    AFFECTS_PORTFOLIO = "AFFECTS_PORTFOLIO"
    AFFECTS_LOAN = "AFFECTS_LOAN"
    USES_SIMULATION = "USES_SIMULATION"
    REFERENCES_TIMELINE = "REFERENCES_TIMELINE"


class DecisionRelationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_decision_id: str
    target_id: str
    target_type: str  # 'DECISION', 'GOAL', 'PORTFOLIO', 'SIMULATION'
    relationship_type: DecisionRelationshipType
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DecisionVersion(BaseModel):
    version: int
    semantic_version: str
    created_at: datetime
    rollback_metadata: Optional[Dict[str, Any]] = None


class Decision(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: DecisionType
    category: DecisionCategory
    status: DecisionStatus = DecisionStatus.DRAFT
    scope: DecisionScope
    priority: DecisionPriority
    version_info: DecisionVersion
    metadata: DecisionMetadata
    provenance: DecisionProvenance
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
