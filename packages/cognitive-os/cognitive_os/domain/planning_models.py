from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TimeHorizon(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    FIVE_YEAR = "FIVE_YEAR"
    RETIREMENT = "RETIREMENT"
    ESTATE_PLANNING = "ESTATE_PLANNING"
    GENERATIONAL_WEALTH = "GENERATIONAL_WEALTH"


class GoalPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class GoalDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the goal")
    title: str = Field(..., description="Short title of the goal")
    description: str = Field(..., description="Detailed description of the goal")
    horizon: TimeHorizon = Field(..., description="Time horizon for the goal")
    priority: GoalPriority = Field(..., description="Priority level of the goal")
    target_amount: Optional[float] = Field(
        None, description="Target financial amount if applicable"
    )
    current_amount: Optional[float] = Field(None, description="Current progress amount")
    dependencies: List[str] = Field(
        default_factory=list, description="IDs of goals this goal depends on"
    )
    status: str = Field(
        default="ACTIVE", description="Status: ACTIVE, COMPLETED, PAUSED, ABANDONED"
    )


class MissionPriority(str, Enum):
    ROUTINE = "ROUTINE"
    ELEVATED = "ELEVATED"
    URGENT = "URGENT"


class MissionDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the mission")
    goal_id: Optional[str] = Field(None, description="The goal this mission supports")
    title: str = Field(..., description="Mission title")
    description: str = Field(..., description="What the mission aims to achieve")
    priority: MissionPriority = Field(
        default=MissionPriority.ROUTINE, description="Execution priority"
    )
    risk_level: str = Field(
        default="LOW", description="Assessed risk level (LOW, MEDIUM, HIGH)"
    )
    financial_impact_estimate: float = Field(
        default=0.0, description="Estimated financial impact in dollars"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Mission IDs that must complete first"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Contextual payload for execution"
    )
    status: str = Field(
        default="PENDING",
        description="Status: PENDING, IN_PROGRESS, REVIEW, COMPLETED, FAILED",
    )
