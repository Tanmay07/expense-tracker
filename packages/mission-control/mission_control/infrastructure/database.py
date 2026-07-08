from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    JSON,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
import enum

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MissionTypeEnum(str, enum.Enum):
    TODAYS_TASKS = "TODAYS_TASKS"
    CRITICAL_ALERTS = "CRITICAL_ALERTS"
    FINANCIAL_WINS = "FINANCIAL_WINS"
    RECOMMENDED_ACTIONS = "RECOMMENDED_ACTIONS"
    UPCOMING_BILLS = "UPCOMING_BILLS"
    INVESTMENT_OPPORTUNITIES = "INVESTMENT_OPPORTUNITIES"
    SAVINGS_SUGGESTIONS = "SAVINGS_SUGGESTIONS"
    BUDGET_ADJUSTMENTS = "BUDGET_ADJUSTMENTS"
    GOAL_MILESTONES = "GOAL_MILESTONES"


class MissionStatusEnum(str, enum.Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    COMPLETED = "COMPLETED"
    DISMISSED = "DISMISSED"
    EXPIRED = "EXPIRED"
    DEFERRED = "DEFERRED"
    ESCALATED = "ESCALATED"


class MissionModel(Base):
    __tablename__ = "mission_control_missions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)
    type = Column(SQLEnum(MissionTypeEnum))
    status = Column(SQLEnum(MissionStatusEnum), default=MissionStatusEnum.CREATED)

    # Priority embedded
    priority_level = Column(String)
    urgency_score = Column(Float)
    financial_impact_score = Column(Float)
    confidence = Column(Float)
    business_impact = Column(String)

    # JSON blobs for complex structures
    explanation = Column(JSON)
    actions = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OpportunityModel(Base):
    __tablename__ = "mission_control_opportunities"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    score = Column(Float)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class RiskModel(Base):
    __tablename__ = "mission_control_risks"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)
    severity = Column(String)
    description = Column(String)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
