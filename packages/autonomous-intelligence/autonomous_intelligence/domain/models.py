import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional
from sqlalchemy import String, JSON, DateTime, ForeignKey, Enum as SQLEnum, Text, Float, Boolean, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Base(DeclarativeBase):
    pass

class RiskClassification(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class GoalType(str, Enum):
    EMERGENCY_FUND = "EMERGENCY_FUND"
    DEBT_REDUCTION = "DEBT_REDUCTION"
    INVESTMENT_GROWTH = "INVESTMENT_GROWTH"
    SAVINGS = "SAVINGS"
    CASH_FLOW = "CASH_FLOW"
    INSURANCE = "INSURANCE"
    TAXES = "TAXES"
    RETIREMENT = "RETIREMENT"
    TRAVEL = "TRAVEL"
    EDUCATION = "EDUCATION"
    CUSTOM = "CUSTOM"

class HITLClassification(str, Enum):
    INFORM = "INFORM"
    RECOMMEND = "RECOMMEND"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    SEMI_AUTOMATED = "SEMI_AUTOMATED"
    FULLY_AUTOMATED = "FULLY_AUTOMATED"

class Agent(Base):
    __tablename__ = "afip_agents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    capabilities: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    allowed_tools: Mapped[List[str]] = mapped_column(JSONB, default=list)
    allowed_sdks: Mapped[List[str]] = mapped_column(JSONB, default=list)
    memory_scope: Mapped[str] = mapped_column(String(100), default="SHARED")
    risk_classification: Mapped[RiskClassification] = mapped_column(SQLEnum(RiskClassification), nullable=False)
    execution_permissions: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    lifecycle_state: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    dependencies: Mapped[List[str]] = mapped_column(JSONB, default=list)
    policies: Mapped[List[str]] = mapped_column(JSONB, default=list)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    metadata_col: Mapped[Dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Goal(Base):
    __tablename__ = "afip_goals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_agents.id"), nullable=False)
    goal_type: Mapped[GoalType] = mapped_column(SQLEnum(GoalType), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    current_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="IN_PROGRESS")
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Mission(Base):
    __tablename__ = "afip_missions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_agents.id"), nullable=False)
    goal_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_goals.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="CREATED")
    plan: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    hitl_classification: Mapped[HITLClassification] = mapped_column(SQLEnum(HITLClassification), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Plan(Base):
    __tablename__ = "afip_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_agents.id"), nullable=False)
    mission_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_missions.id"), nullable=True)
    horizon: Mapped[str] = mapped_column(String(50), nullable=False) # DAILY, WEEKLY, MONTHLY, ANNUAL, MULTI_YEAR
    content: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    is_contingency: Mapped[bool] = mapped_column(Boolean, default=False)
    is_alternative: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Memory(Base):
    __tablename__ = "afip_memories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_agents.id"), nullable=False)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False) # WORKING, EPISODIC, LONG_TERM, SHARED
    reference_id: Mapped[str] = mapped_column(String(255), nullable=True) # pointer to Knowledge Graph or Timeline
    content: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Evaluation(Base):
    __tablename__ = "afip_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_agents.id"), nullable=False)
    mission_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("afip_missions.id"), nullable=True)
    
    goal_completion_score: Mapped[float] = mapped_column(Float, default=0.0)
    financial_impact: Mapped[float] = mapped_column(Float, default=0.0)
    recommendation_acceptance_rate: Mapped[float] = mapped_column(Float, default=0.0)
    execution_success_rate: Mapped[float] = mapped_column(Float, default=0.0)
    ai_quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    trust_score: Mapped[float] = mapped_column(Float, default=0.0)
    user_satisfaction_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    evaluation_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    evaluation_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
