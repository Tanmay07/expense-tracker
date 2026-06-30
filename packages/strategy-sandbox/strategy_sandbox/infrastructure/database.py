import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Float, Integer, DateTime,
    ForeignKey, ARRAY
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ValidationProfileModel(Base):
    """
    Reusable profiles configuring the pipeline stages, criteria, and timeouts.
    """
    __tablename__ = "sandbox_validation_profiles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    profile_type = Column(String, nullable=False) # e.g. INVESTMENT_STRATEGY, AI_PROMPT
    
    required_stages = Column(ARRAY(String), nullable=False)
    pass_criteria_json = Column(JSONB, nullable=False, default=dict)
    failure_thresholds_json = Column(JSONB, nullable=False, default=dict)
    scoring_weights_json = Column(JSONB, nullable=False, default=dict)
    
    timeout_seconds = Column(Integer, default=3600)
    approval_requirements = Column(ARRAY(String), default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    runs = relationship("SandboxRunModel", back_populates="profile")


class SandboxRunModel(Base):
    """
    Specific execution of a validation pipeline on an asset.
    """
    __tablename__ = "sandbox_runs"

    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False) # Refers to MarketplaceAsset or external artifact
    profile_id = Column(String, ForeignKey("sandbox_validation_profiles.id"), nullable=False)
    
    status = Column(String, nullable=False, default="PENDING") # PENDING, IN_PROGRESS, PASSED, FAILED, TIMEOUT
    current_stage = Column(String, nullable=True)
    
    stage_results_json = Column(JSONB, nullable=False, default=dict)
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    profile = relationship("ValidationProfileModel", back_populates="runs")
    fitness_score = relationship("FitnessScoreModel", back_populates="run", uselist=False, cascade="all, delete-orphan")
    prompt_validation = relationship("PromptValidationModel", back_populates="run", uselist=False, cascade="all, delete-orphan")
    benchmark = relationship("BenchmarkRecordModel", back_populates="run", uselist=False, cascade="all, delete-orphan")
    replay_snapshot = relationship("ReplaySnapshotModel", back_populates="run", uselist=False, cascade="all, delete-orphan")
    certification = relationship("SandboxCertificationModel", back_populates="run", uselist=False, cascade="all, delete-orphan")


class FitnessScoreModel(Base):
    """
    Composite score calculating the strategy's fitness for production.
    """
    __tablename__ = "sandbox_fitness_scores"

    id = Column(String, primary_key=True)
    run_id = Column(String, ForeignKey("sandbox_runs.id"), nullable=False, unique=True)
    
    financial_impact = Column(Float, default=0.0)
    risk_adjusted_return = Column(Float, default=0.0)
    goal_completion_probability = Column(Float, default=0.0)
    policy_compliance = Column(Float, default=0.0)
    downside_risk = Column(Float, default=0.0)
    simulation_stability = Column(Float, default=0.0)
    historical_consistency = Column(Float, default=0.0)
    explainability_quality = Column(Float, default=0.0)
    ai_confidence = Column(Float, default=0.0)
    execution_complexity = Column(Float, default=0.0)
    
    composite_score = Column(Float, nullable=False)
    
    run = relationship("SandboxRunModel", back_populates="fitness_score")


class BenchmarkRecordModel(Base):
    """
    Regression reports and comparison scores against baselines.
    """
    __tablename__ = "sandbox_benchmarks"

    id = Column(String, primary_key=True)
    run_id = Column(String, ForeignKey("sandbox_runs.id"), nullable=False, unique=True)
    
    benchmark_type = Column(String, nullable=False) # BASELINE, HISTORICAL, COMMUNITY
    reference_id = Column(String, nullable=True)
    
    regression_report_json = Column(JSONB, nullable=False, default=dict)
    improvement_analysis_json = Column(JSONB, nullable=False, default=dict)

    run = relationship("SandboxRunModel", back_populates="benchmark")


class PromptValidationModel(Base):
    """
    Specific validation metrics for AI prompts evaluated by LiteLLM.
    """
    __tablename__ = "sandbox_prompt_validations"

    id = Column(String, primary_key=True)
    run_id = Column(String, ForeignKey("sandbox_runs.id"), nullable=False, unique=True)
    
    hallucination_resistance = Column(Float, default=0.0)
    policy_compliance = Column(Float, default=0.0)
    tool_selection_accuracy = Column(Float, default=0.0)
    output_consistency = Column(Float, default=0.0)
    explainability = Column(Float, default=0.0)
    
    latency_ms = Column(Integer, default=0)
    token_usage = Column(Integer, default=0)
    model_compatibility = Column(ARRAY(String), default=list)

    run = relationship("SandboxRunModel", back_populates="prompt_validation")


class ReplaySnapshotModel(Base):
    """
    Persisted metadata to replay validations deterministically.
    """
    __tablename__ = "sandbox_replay_snapshots"

    id = Column(String, primary_key=True)
    run_id = Column(String, ForeignKey("sandbox_runs.id"), nullable=False, unique=True)
    
    input_snapshot_json = Column(JSONB, nullable=False, default=dict)
    timeline_snapshot_json = Column(JSONB, nullable=False, default=dict)
    knowledge_graph_snapshot_json = Column(JSONB, nullable=False, default=dict)
    
    digital_twin_version = Column(String, nullable=True)
    prompt_version = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    
    simulation_seed = Column(String, nullable=False)
    validation_configuration_json = Column(JSONB, nullable=False, default=dict)

    run = relationship("SandboxRunModel", back_populates="replay_snapshot")


class SandboxCertificationModel(Base):
    """
    Internal certification assigned before an artifact can hit the Marketplace.
    """
    __tablename__ = "sandbox_certifications"

    id = Column(String, primary_key=True)
    run_id = Column(String, ForeignKey("sandbox_runs.id"), nullable=False, unique=True)
    
    asset_id = Column(String, nullable=False)
    certification_level = Column(String, nullable=False) # EXPERIMENTAL, INTERNAL, CERTIFIED, ENTERPRISE_CERTIFIED, REGULATED
    
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    review_schedule_json = Column(JSONB, nullable=False, default=dict)

    run = relationship("SandboxRunModel", back_populates="certification")
