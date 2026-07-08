import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    ARRAY,
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


class ArtifactRecordModel(Base):
    """
    Core metadata for a registered validation artifact.
    """

    __tablename__ = "var_artifact_records"

    id = Column(String, primary_key=True)
    canonical_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(
        String, nullable=False
    )  # e.g. VALIDATION_REPORT, MONTE_CARLO_OUTPUT, REPLAY_PACKAGE
    producer = Column(String, nullable=False)

    pipeline_id = Column(String, nullable=True)
    sandbox_run_id = Column(String, nullable=True)
    strategy_id = Column(String, nullable=True)

    version = Column(String, nullable=False, default="1.0.0")
    status = Column(
        String, nullable=False, default="ACTIVE"
    )  # ACTIVE, DEPRECATED, ARCHIVED, PURGED
    owner_id = Column(String, nullable=False)

    tags = Column(ARRAY(String), default=list)
    metadata_json = Column(JSONB, nullable=False, default=dict)

    # Storage and Integrity
    storage_location = Column(String, nullable=False)  # URI to S3 or local disk
    checksum_sha256 = Column(String, nullable=False)
    digital_signature = Column(String, nullable=True)
    is_encrypted = Column(Boolean, default=False)
    is_compressed = Column(Boolean, default=False)
    integrity_status = Column(String, default="VERIFIED")  # VERIFIED, VIOLATION

    # Lifecycle
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    retention_policy = Column(String, nullable=False, default="30_DAYS")

    lineage_sources = relationship(
        "ArtifactLineageModel",
        foreign_keys="[ArtifactLineageModel.target_id]",
        back_populates="target",
    )
    lineage_targets = relationship(
        "ArtifactLineageModel",
        foreign_keys="[ArtifactLineageModel.source_id]",
        back_populates="source",
    )

    UniqueConstraint("canonical_name", "version", name="uq_artifact_version")


class ArtifactLineageModel(Base):
    """
    Relational edge representing a directed graph of artifact lineage.
    source_id (e.g. SandboxRun Artifact) -> target_id (e.g. Evidence Package)
    """

    __tablename__ = "var_artifact_lineage"

    id = Column(String, primary_key=True)
    source_id = Column(String, ForeignKey("var_artifact_records.id"), nullable=False)
    target_id = Column(String, ForeignKey("var_artifact_records.id"), nullable=False)
    relationship_type = Column(
        String, nullable=False
    )  # DERIVED_FROM, BUNDLED_IN, VALIDATED_BY

    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship(
        "ArtifactRecordModel",
        foreign_keys=[source_id],
        back_populates="lineage_targets",
    )
    target = relationship(
        "ArtifactRecordModel",
        foreign_keys=[target_id],
        back_populates="lineage_sources",
    )

    UniqueConstraint(
        "source_id", "target_id", "relationship_type", name="uq_lineage_edge"
    )


class EvidencePackageModel(Base):
    """
    A signed bundle of artifacts grouped for compliance or certification.
    """

    __tablename__ = "var_evidence_packages"

    id = Column(String, primary_key=True)
    package_name = Column(String, nullable=False, unique=True)

    # Array of ArtifactRecord IDs
    artifact_ids = Column(ARRAY(String), nullable=False)

    certification_id = Column(String, nullable=True)
    compliance_framework = Column(String, nullable=True)

    digital_signature = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReuseEvaluationModel(Base):
    """
    Tracks equivalency evaluations to determine if an artifact can be safely reused instead of recomputing.
    """

    __tablename__ = "var_reuse_evaluations"

    id = Column(String, primary_key=True)
    target_artifact_id = Column(
        String, ForeignKey("var_artifact_records.id"), nullable=False
    )

    input_hash = Column(String, nullable=False)
    policy_version = Column(String, nullable=True)
    model_version = Column(String, nullable=True)

    is_reusable = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=False)
    reason = Column(String, nullable=True)

    evaluated_at = Column(DateTime, default=datetime.utcnow)
