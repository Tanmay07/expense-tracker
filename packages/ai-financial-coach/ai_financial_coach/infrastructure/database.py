from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Integer,
    JSON,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
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


class MemoryItemTypeEnum(enum.Enum):
    PREFERENCE = "PREFERENCE"
    FACT = "FACT"
    DECISION = "DECISION"
    BEHAVIOR = "BEHAVIOR"


class ConversationModel(Base):
    __tablename__ = "ai_conversations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    context_summaries = Column(JSON)  # List of strings


class MessageModel(Base):
    __tablename__ = "ai_messages"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    role = Column(String)  # user, assistant, system, tool
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    name = Column(String, nullable=True)
    tool_calls = Column(JSON, nullable=True)
    explainability_metadata = Column(JSON, nullable=True)


class MemoryItemModel(Base):
    __tablename__ = "ai_memories"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    type = Column(SQLEnum(MemoryItemTypeEnum))
    content = Column(String)
    embedding = Column(Vector(1536))  # OpenAI embedding size
    created_at = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=True)
    confidence_score = Column(Float, default=1.0)


class PromptTemplateModel(Base):
    __tablename__ = "ai_prompt_templates"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    template = Column(String)
    version = Column(Integer, default=1)
    description = Column(String)
    tags = Column(JSON)


class AgentDefinitionModel(Base):
    __tablename__ = "ai_agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    system_prompt = Column(String)
    tools = Column(JSON)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
