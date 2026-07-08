from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    SUPERVISOR = "SUPERVISOR"
    BUDGET = "BUDGET"
    CASH_FLOW = "CASH_FLOW"
    INVESTMENT = "INVESTMENT"
    DEBT_OPTIMIZATION = "DEBT_OPTIMIZATION"
    INSURANCE = "INSURANCE"
    TAX_PLANNING = "TAX_PLANNING"
    GOAL_PLANNING = "GOAL_PLANNING"
    MISSION_PLANNING = "MISSION_PLANNING"
    RISK = "RISK"
    FORECASTING = "FORECASTING"
    FRAUD_DETECTION = "FRAUD_DETECTION"
    MERCHANT_INTELLIGENCE = "MERCHANT_INTELLIGENCE"
    NOTIFICATION = "NOTIFICATION"
    ADVISOR_ASSISTANT = "ADVISOR_ASSISTANT"
    HOUSEHOLD_COORDINATION = "HOUSEHOLD_COORDINATION"
    LEARNING = "LEARNING"
    GOVERNANCE_OBSERVER = "GOVERNANCE_OBSERVER"


class MemoryScope(str, Enum):
    EPHEMERAL = "EPHEMERAL"  # Cleared after mission
    MISSION = "MISSION"  # Persists for mission lifecycle
    LONG_TERM = "LONG_TERM"  # Persists indefinitely in Knowledge Graph


class AgentDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the agent configuration")
    role: AgentRole = Field(..., description="The role this agent fulfills")
    capabilities: List[str] = Field(
        default_factory=list, description="List of capabilities this agent possesses"
    )
    allowed_tools: List[str] = Field(
        default_factory=list, description="List of MCP tools or SDK functions allowed"
    )
    memory_scope: MemoryScope = Field(
        default=MemoryScope.MISSION, description="Scope of agent's working memory"
    )
    escalation_rules: List[str] = Field(
        default_factory=list, description="Rules for escalating to supervisor or human"
    )
    approval_requirements: List[str] = Field(
        default_factory=list, description="Conditions requiring explicit human approval"
    )
    policies: List[str] = Field(
        default_factory=list, description="List of policy IDs this agent must adhere to"
    )
    description: str = Field(
        ..., description="Human-readable description of the agent's purpose"
    )
