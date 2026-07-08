from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from enum import Enum


class PolicyCategory(str, Enum):
    EXECUTION = "EXECUTION"
    AUTOMATION = "AUTOMATION"
    RISK = "RISK"
    COMPLIANCE = "COMPLIANCE"
    APPROVAL = "APPROVAL"


class EvaluationOutcome(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    DEFER = "DEFER"
    ESCALATE = "ESCALATE"


class RuleOperator(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    GT = "GT"
    LT = "LT"
    GTE = "GTE"
    LTE = "LTE"
    CONTAINS = "CONTAINS"
    IN = "IN"
    NOT_IN = "NOT_IN"
    AND = "AND"
    OR = "OR"


class RuleAST(BaseModel):
    operator: RuleOperator
    # Field to check in the context, e.g., "decision.amount"
    field: Optional[str] = None
    # Expected value to compare against
    value: Optional[Any] = None
    # For nested rules (AND/OR)
    conditions: Optional[List["RuleAST"]] = None


class ExecutionPolicy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: PolicyCategory
    version: int = 1
    priority: int = 100
    rule_ast: RuleAST
    outcome_if_matched: EvaluationOutcome
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PolicyExplanation(BaseModel):
    triggering_policy_id: Optional[str] = None
    triggering_policy_name: Optional[str] = None
    matched_conditions: List[str] = Field(default_factory=list)
    human_readable: str


class EvaluationResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    outcome: EvaluationOutcome
    explanation: PolicyExplanation
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


class PolicyContext(BaseModel):
    request_id: str
    decision_metadata: Dict[str, Any]
    capability_metadata: Dict[str, Any]
    user_metadata: Dict[str, Any]
    risk_profile: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
