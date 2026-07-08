from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Integer,
    Boolean,
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


class RiskLevelEnum(enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DecisionStatusEnum(enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    WARNING = "WARNING"


class PolicyTypeEnum(enum.Enum):
    ALLOCATION = "ALLOCATION"
    RISK = "RISK"
    TAX = "TAX"
    LIQUIDITY = "LIQUIDITY"
    CURRENCY = "CURRENCY"
    BROKER = "BROKER"
    CUSTOM = "CUSTOM"


class PolicySeverityEnum(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"


class RiskProfileModel(Base):
    __tablename__ = "compliance_risk_profiles"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    risk_capacity = Column(Float)
    risk_tolerance = Column(Float)
    investment_horizon_years = Column(Integer)
    liquidity_needs = Column(Float)
    income_stability_score = Column(Float)
    emergency_fund_ratio = Column(Float)
    overall_risk_level = Column(SQLEnum(RiskLevelEnum))
    updated_at = Column(DateTime, default=datetime.utcnow)


class CompliancePolicyModel(Base):
    __tablename__ = "compliance_policies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(SQLEnum(PolicyTypeEnum))
    description = Column(String)
    severity = Column(SQLEnum(PolicySeverityEnum))
    rule_expression = Column(String)
    parameters = Column(JSON)
    jurisdiction = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)


class SuitabilityProfileModel(Base):
    __tablename__ = "compliance_suitability_profiles"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    suitability_score = Column(Float)
    confidence_score = Column(Float)
    last_evaluated_at = Column(DateTime, default=datetime.utcnow)
    factors = Column(JSON)


class InvestmentConstraintModel(Base):
    __tablename__ = "compliance_investment_constraints"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    constraint_type = Column(String)
    target = Column(String)
    operator = Column(String)
    value = Column(JSON)


class DecisionRecordModel(Base):
    __tablename__ = "compliance_decision_records"

    id = Column(String, primary_key=True, index=True)
    context_id = Column(String, index=True)
    action_type = Column(String)
    status = Column(SQLEnum(DecisionStatusEnum))
    confidence = Column(Float)
    policies_evaluated = Column(JSON)  # List of strings
    rules_triggered = Column(JSON)  # List of strings
    explanation = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    audit_trail = Column(JSON)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
