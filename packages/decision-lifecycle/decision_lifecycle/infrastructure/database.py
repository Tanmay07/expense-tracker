from sqlalchemy import create_engine, Column, String, Float, JSON, DateTime
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


class DecisionLifecycleModel(Base):
    __tablename__ = "lifecycle_states"

    id = Column(String, primary_key=True, index=True)
    decision_id = Column(String, index=True, unique=True)
    current_state = Column(String)
    state_history = Column(JSON)
    objective_id = Column(String, nullable=True)
    execution_plan_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ObjectiveModel(Base):
    __tablename__ = "lifecycle_objectives"

    id = Column(String, primary_key=True, index=True)
    canonical_name = Column(String)
    category = Column(String)
    weight = Column(Float)
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    metadata_json = Column(JSON)


class ExecutionPlanModel(Base):
    __tablename__ = "lifecycle_execution_plans"

    id = Column(String, primary_key=True, index=True)
    decision_id = Column(String, index=True)
    steps_json = Column(JSON)
    milestones_json = Column(JSON)
    rollback_plan_json = Column(JSON, nullable=True)
    estimated_duration_days = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
