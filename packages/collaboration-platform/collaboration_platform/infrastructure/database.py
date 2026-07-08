from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    JSON,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime
import enum
import os

Base = declarative_base()


class MemberRole(str, enum.Enum):
    OWNER = "OWNER"
    CO_OWNER = "CO_OWNER"
    DEPENDENT = "DEPENDENT"
    ADVISOR = "ADVISOR"
    VIEWER = "VIEWER"


class DelegationScope(str, enum.Enum):
    VIEW_ONLY = "VIEW_ONLY"
    COMMENT = "COMMENT"
    RECOMMEND = "RECOMMEND"
    MANAGE_BUDGETS = "MANAGE_BUDGETS"
    EXECUTE_ACTIONS = "EXECUTE_ACTIONS"
    FULL_ADMIN = "FULL_ADMIN"


class MissionStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class HouseholdModel(Base):
    __tablename__ = "households"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    settings = Column(JSON, default=dict)


class HouseholdMemberModel(Base):
    __tablename__ = "household_members"
    id = Column(String, primary_key=True)
    household_id = Column(String, ForeignKey("households.id"))
    user_id = Column(String, nullable=False)
    role = Column(SQLEnum(MemberRole), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class AdvisorModel(Base):
    __tablename__ = "advisors"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    firm_name = Column(String, nullable=True)
    specialty = Column(String, nullable=False)
    certification_details = Column(JSON, default=dict)


class DelegationModel(Base):
    __tablename__ = "delegations"
    id = Column(String, primary_key=True)
    delegator_user_id = Column(String, nullable=False)
    delegatee_user_id = Column(String, nullable=False)
    scope = Column(SQLEnum(DelegationScope), nullable=False)
    household_id = Column(String, ForeignKey("households.id"), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class SharedWorkspaceModel(Base):
    __tablename__ = "shared_workspaces"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    household_id = Column(String, ForeignKey("households.id"), nullable=True)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SharedMissionModel(Base):
    __tablename__ = "shared_missions"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, ForeignKey("shared_workspaces.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(MissionStatus), default=MissionStatus.PROPOSED)
    owners = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True)
    thread_id = Column(String, nullable=False)
    sender_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    read_by = Column(JSON, default=list)


class HouseholdPolicyModel(Base):
    __tablename__ = "household_policies"
    id = Column(String, primary_key=True)
    household_id = Column(String, ForeignKey("households.id"))
    policy_type = Column(String, nullable=False)
    rules = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


DATABASE_URL = os.getenv(
    "COLLABORATION_DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/finance_os_collaboration",
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with async_session_maker() as session:
        yield session
