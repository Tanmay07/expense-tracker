from sqlalchemy import create_engine, Column, String, Float, Integer, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DecisionModel(Base):
    __tablename__ = "registry_decisions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    type = Column(String)
    category = Column(String)
    status = Column(String)
    scope = Column(String)

    # Priority
    priority_level = Column(String)
    importance_score = Column(Float)

    # Versioning
    version = Column(Integer)
    semantic_version = Column(String)
    rollback_metadata = Column(JSON, nullable=True)

    # Complex Aggregates (JSONB equivalent)
    metadata_json = Column(JSON)
    provenance_json = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DecisionRelationshipModel(Base):
    __tablename__ = "registry_decision_relationships"

    id = Column(String, primary_key=True, index=True)
    source_decision_id = Column(String, index=True)
    target_id = Column(String, index=True)
    target_type = Column(String)
    relationship_type = Column(String)
    metadata_json = Column(JSON)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
