from sqlalchemy import create_engine, Column, String, Boolean, JSON, DateTime, Integer
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


class PolicyModel(Base):
    __tablename__ = "execution_policies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    version = Column(Integer, default=1)
    priority = Column(Integer, default=100)
    rule_ast_json = Column(JSON)
    outcome_if_matched = Column(String)
    is_active = Column(Boolean, default=True)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class EvaluationLogModel(Base):
    __tablename__ = "policy_evaluation_logs"

    id = Column(String, primary_key=True, index=True)
    request_id = Column(String, index=True)
    outcome = Column(String)
    explanation_json = Column(JSON)
    evaluated_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
