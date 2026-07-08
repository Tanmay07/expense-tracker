import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class FeatureModel(Base):
    """
    Universal Registry for any deployable capability.
    """

    __tablename__ = "exp_features"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    version = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # AI_MODEL, PROMPT, UI_COMPONENT, ALGORITHM
    feature_type = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)

    dependencies = Column(JSONB, nullable=True)  # list of other feature IDs

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FeatureFlagModel(Base):
    """
    Runtime evaluation rules for a feature.
    """

    __tablename__ = "exp_feature_flags"

    id = Column(String, primary_key=True)
    feature_id = Column(
        String, ForeignKey("exp_features.id"), nullable=False, index=True
    )

    # BOOLEAN, PERCENTAGE, TARGETING
    flag_type = Column(String, nullable=False)

    # Is the flag completely disabled? (Kill switch)
    is_enabled = Column(Boolean, default=False)

    # If BOOLEAN
    default_value = Column(Boolean, nullable=True)

    # If PERCENTAGE
    rollout_percentage = Column(Float, nullable=True)

    # If TARGETING (JSONLogic or custom schema)
    targeting_rules_json = Column(JSONB, nullable=True)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RolloutModel(Base):
    """
    Tracks progressive delivery state.
    """

    __tablename__ = "exp_rollouts"

    id = Column(String, primary_key=True)
    feature_id = Column(
        String, ForeignKey("exp_features.id"), nullable=False, index=True
    )

    # DISABLED, INTERNAL, ALPHA, BETA, CANARY, GLOBAL
    current_stage = Column(String, nullable=False)

    # E.g. {"alpha_group_ids": ["dev1", "dev2"]}
    stage_metadata_json = Column(JSONB, nullable=True)

    is_paused = Column(Boolean, default=False)

    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExperimentModel(Base):
    """
    A/B Tests, Multi-armed bandits, prompt comparisons.
    """

    __tablename__ = "exp_experiments"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    # AB_TEST, MAB, AI_PROMPT_COMPARISON
    experiment_type = Column(String, nullable=False)

    # JSON containing variants (e.g. {"control": "feat_a", "variant_1": "feat_b"})
    variants_json = Column(JSONB, nullable=False)

    # Allocation weights (e.g. {"control": 50, "variant_1": 50})
    weights_json = Column(JSONB, nullable=False)

    # Metrics to optimize for (e.g. ["latency", "acceptance_rate", "hallucination_score"])
    target_metrics = Column(JSONB, nullable=False)

    status = Column(
        String, nullable=False, default="DRAFT"
    )  # DRAFT, RUNNING, PAUSED, COMPLETED

    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)


class ExperimentResultModel(Base):
    """
    Aggregated analytics linked to an experiment.
    """

    __tablename__ = "exp_experiment_results"

    id = Column(String, primary_key=True)
    experiment_id = Column(
        String, ForeignKey("exp_experiments.id"), nullable=False, index=True
    )

    # JSON containing aggregated results per variant
    results_json = Column(JSONB, nullable=False)

    # ID of the winning variant, if conclusively determined
    winning_variant_id = Column(String, nullable=True)

    calculated_at = Column(DateTime, default=datetime.utcnow)
