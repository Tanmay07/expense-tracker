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
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class GovernancePolicyModel(Base):
    """
    Declarative Governance-as-Code policies defining rules for asset promotion.
    """

    __tablename__ = "gov_policies"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    domain = Column(String, nullable=False)
    version = Column(String, nullable=False, default="1.0.0")

    # Store policy payload in JSON format (OPA compatible future state)
    policy_payload_json = Column(JSONB, nullable=False)

    status = Column(
        String, nullable=False, default="DRAFT"
    )  # DRAFT, ACTIVE, DEPRECATED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    UniqueConstraint("name", "version", name="uq_policy_version")


class TrustScoreModel(Base):
    """
    Dynamic Trust rating assigned to assets across the OS.
    """

    __tablename__ = "gov_trust_scores"

    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False, index=True)

    # Granular scoring dimensions
    validation_score = Column(Float, default=0.0)
    lineage_score = Column(Float, default=0.0)
    ai_confidence_score = Column(Float, default=0.0)
    policy_compliance_score = Column(Float, default=0.0)
    marketplace_usage_score = Column(Float, default=0.0)

    # Computed aggregate
    composite_trust_score = Column(Float, nullable=False, default=0.0)

    is_trusted = Column(Boolean, default=False)
    last_calculated_at = Column(DateTime, default=datetime.utcnow)


class MaturityRecordModel(Base):
    """
    Tracks the lifecycle maturity stage of an asset (e.g., Experimental -> Production).
    """

    __tablename__ = "gov_maturity_records"

    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False, index=True)

    current_level = Column(String, nullable=False, default="EXPERIMENTAL")
    # EXPERIMENTAL, INTERNAL, PILOT, PRODUCTION, ENTERPRISE, REGULATED, DEPRECATED

    promoted_at = Column(DateTime, default=datetime.utcnow)
    promoted_by = Column(String, nullable=False)
    reason = Column(String, nullable=True)


class AIGovernanceModel(Base):
    """
    Tracks safety, alignment, and compliance metrics for AI models and prompts.
    """

    __tablename__ = "gov_ai_metrics"

    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False, index=True)  # Usually a prompt or model

    hallucination_rate = Column(Float, default=0.0)
    bias_score = Column(Float, default=0.0)
    fairness_score = Column(Float, default=0.0)
    prompt_drift = Column(Float, default=0.0)
    privacy_violation_count = Column(Float, default=0.0)

    evaluated_at = Column(DateTime, default=datetime.utcnow)


class EvidenceLedgerModel(Base):
    """
    Immutable ledger of evidence hashes and digital signatures.
    """

    __tablename__ = "gov_evidence_ledger"

    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False, index=True)
    evidence_type = Column(
        String, nullable=False
    )  # e.g., SANDBOX_PASS, MANUAL_APPROVAL

    # The cryptographic digest of the evidence payload
    payload_hash = Column(String, nullable=False)
    digital_signature = Column(String, nullable=False)
    signer_id = Column(String, nullable=False)

    # Link to the previous ledger entry for the asset to form a hash chain (Merkle concept)
    previous_ledger_id = Column(
        String, ForeignKey("gov_evidence_ledger.id"), nullable=True
    )

    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to traverse the chain if needed
    previous_record = relationship("EvidenceLedgerModel", remote_side=[id])


class WorkflowStateModel(Base):
    """
    State machine for governance approval workflows.
    """

    __tablename__ = "gov_workflows"

    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False, index=True)
    workflow_type = Column(String, nullable=False)  # e.g., PRODUCTION_PROMOTION

    current_state = Column(
        String, nullable=False, default="DRAFT"
    )  # DRAFT, REVIEW, APPROVED, REJECTED
    assigned_reviewer_id = Column(String, nullable=True)

    comments = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
