from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Boolean,
    JSON,
    DateTime,
    Integer,
    Text,
    ARRAY,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
from pgvector.sqlalchemy import Vector

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DecisionMemoryModel(Base):
    __tablename__ = "decision_memory"

    id = Column(String, primary_key=True, index=True)
    decision_id = Column(String, index=True)
    user_id = Column(String, index=True)
    action_type = Column(String, index=True)
    evidence_json = Column(JSON)
    context_snapshot_json = Column(JSON)
    policy_snapshot_json = Column(JSON)
    timeline_snapshot_version = Column(Integer)
    knowledge_graph_snapshot_version = Column(Integer)
    simulation_snapshot_id = Column(String)
    financial_metrics_json = Column(JSON)
    prompt_version = Column(String)
    model_version = Column(String)
    execution_outcome = Column(String)
    user_feedback_score = Column(Float)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, default=datetime.utcnow)


class PatternModel(Base):
    __tablename__ = "learning_patterns"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    pattern_type = Column(String, index=True)
    description = Column(Text)
    confidence = Column(Float)
    evidence_events = Column(ARRAY(String))
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class PersonalizationModel(Base):
    __tablename__ = "adaptive_personalizations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, unique=True)
    preferred_strategies_json = Column(JSON)
    communication_style = Column(String)
    risk_preference = Column(String)
    recommendation_frequency = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PolicyCacheModel(Base):
    __tablename__ = "policy_decision_cache"

    id = Column(String, primary_key=True, index=True)
    decision_id = Column(String, index=True)
    policy_version = Column(Integer)
    context_snapshot_id = Column(String)
    evaluation_result = Column(String)
    expires_at = Column(DateTime)
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class PredictionModel(Base):
    __tablename__ = "decision_predictions"

    id = Column(String, primary_key=True, index=True)
    decision_id = Column(String, index=True)
    user_id = Column(String, index=True)
    acceptance_probability = Column(Float)
    completion_probability = Column(Float)
    expected_roi = Column(Float)
    risk_reduction = Column(Float)
    confidence_interval_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class FinancialDNAModel(Base):
    __tablename__ = "financial_dna_profiles"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, unique=True)
    investor_type = Column(String)
    saver_type = Column(String)
    debt_discipline_score = Column(Float)
    risk_appetite_score = Column(Float)
    impulse_spending_index = Column(Float)
    goal_discipline_score = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BehaviorModel(Base):
    __tablename__ = "behavioral_evolutions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    evolution_type = Column(String)
    previous_value = Column(String)
    new_value = Column(String)
    reasoning = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class LearningModel(Base):
    __tablename__ = "continuous_learnings"

    id = Column(String, primary_key=True, index=True)
    learning_type = Column(String)
    target_id = Column(String)
    weight_adjustments_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReplayModel(Base):
    __tablename__ = "learning_replays"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    replay_data_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
