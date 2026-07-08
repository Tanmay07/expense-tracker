from sqlalchemy import Column, String, DateTime, Boolean, JSON, Float, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime
import enum
import os

Base = declarative_base()


class ConsentStatus(str, enum.Enum):
    GRANTED = "GRANTED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"


class RiskCategory(str, enum.Enum):
    FINANCIAL = "FINANCIAL"
    SECURITY = "SECURITY"
    OPERATIONAL = "OPERATIONAL"
    PRIVACY = "PRIVACY"
    COMPLIANCE = "COMPLIANCE"
    AI = "AI"


class PrivacyRequestType(str, enum.Enum):
    ACCESS = "ACCESS"
    RECTIFICATION = "RECTIFICATION"
    ERASURE = "ERASURE"
    PORTABILITY = "PORTABILITY"
    RESTRICT_PROCESSING = "RESTRICT_PROCESSING"


class TrustPolicyModel(Base):
    __tablename__ = "trust_policies"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    rules = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrustScoreModel(Base):
    __tablename__ = "trust_scores"
    id = Column(String, primary_key=True)
    entity_id = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    factors = Column(JSON, default=dict)
    evaluated_at = Column(DateTime, default=datetime.utcnow)


class ConsentRecordModel(Base):
    __tablename__ = "consent_records"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    status = Column(SQLEnum(ConsentStatus), nullable=False)
    version = Column(Float, default=1.0)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class PrivacyRequestModel(Base):
    __tablename__ = "privacy_requests"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    request_type = Column(SQLEnum(PrivacyRequestType), nullable=False)
    status = Column(String, default="PENDING")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class ComplianceProfileModel(Base):
    __tablename__ = "compliance_profiles"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    controls = Column(JSON, default=list)


class AITrustRecordModel(Base):
    __tablename__ = "ai_trust_records"
    id = Column(String, primary_key=True)
    capability_used = Column(String, nullable=False)
    reasoning_summary = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    safety_checks = Column(JSON, default=dict)
    bias_evaluation = Column(JSON, default=dict)
    approval_required = Column(Boolean, default=False)
    executed_at = Column(DateTime, default=datetime.utcnow)


class RiskScoreModel(Base):
    __tablename__ = "risk_scores"
    id = Column(String, primary_key=True)
    target_id = Column(String, nullable=False)
    category = Column(SQLEnum(RiskCategory), nullable=False)
    score = Column(Float, nullable=False)
    evaluated_at = Column(DateTime, default=datetime.utcnow)


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    event_type = Column(String, nullable=False)
    actor_id = Column(String, nullable=False)
    target_id = Column(String, nullable=True)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column("metadata", JSON, default=dict)
    is_immutable = Column(Boolean, default=True)


DATABASE_URL = os.getenv(
    "TRUST_DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/finance_os_trust",
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with async_session_maker() as session:
        yield session
