import uuid
import hashlib
from datetime import datetime, timedelta
from typing import List

from validation_registry.domain.models import (
    ArtifactRecord,
    ArtifactRecordCreate,
    ArtifactLineage,
    EvidencePackage,
    ReuseEvaluation,
)
from validation_registry.infrastructure.repositories import (
    ArtifactRepository,
    ArtifactLineageRepository,
    EvidenceRepository,
    ReuseRepository,
)


class ArtifactStorageService:
    """
    Manages the binary blob storage of artifacts.
    Implements a fallback to local disk if S3 is unavailable.
    """

    def __init__(self, base_dir: str = "/app/data/artifacts"):
        self.base_dir = base_dir

    def store_payload(self, artifact_id: str, payload_bytes: bytes) -> str:
        # Simple local storage fallback mimicking S3 PutObject
        import os

        os.makedirs(self.base_dir, exist_ok=True)
        path = os.path.join(self.base_dir, artifact_id)
        with open(path, "wb") as f:
            f.write(payload_bytes)
        return f"local://{path}"


class IntegrityService:
    """
    Handles cryptographic hashes for evidence tamper detection.
    """

    @staticmethod
    def calculate_sha256(payload_bytes: bytes) -> str:
        return hashlib.sha256(payload_bytes).hexdigest()

    @staticmethod
    def sign_package(artifact_ids: List[str]) -> str:
        # Mocking a digital signature using a combined hash of all IDs
        combined = "".join(sorted(artifact_ids)).encode("utf-8")
        return f"sig_{hashlib.sha256(combined).hexdigest()[:16]}"


class ArtifactRegistryService:
    def __init__(
        self,
        repo: ArtifactRepository,
        storage: ArtifactStorageService,
        integrity: IntegrityService,
    ):
        self.repo = repo
        self.storage = storage
        self.integrity = integrity

    def register_artifact(
        self, dto: ArtifactRecordCreate, payload_bytes: bytes
    ) -> ArtifactRecord:
        artifact_id = f"art_{uuid.uuid4().hex}"

        checksum = self.integrity.calculate_sha256(payload_bytes)
        storage_uri = self.storage.store_payload(artifact_id, payload_bytes)

        # Calculate expiration based on retention policy
        expires_at = None
        if dto.retention_policy == "30_DAYS":
            expires_at = datetime.utcnow() + timedelta(days=30)

        record = ArtifactRecord(
            id=artifact_id,
            canonical_name=dto.canonical_name,
            description=dto.description,
            category=dto.category,
            producer=dto.producer,
            pipeline_id=dto.pipeline_id,
            sandbox_run_id=dto.sandbox_run_id,
            strategy_id=dto.strategy_id,
            version=dto.version,
            owner_id=dto.owner_id,
            tags=dto.tags,
            metadata_json=dto.metadata_json,
            storage_location=storage_uri,
            checksum_sha256=checksum,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            retention_policy=dto.retention_policy,
        )
        return self.repo.save(record)


class ArtifactLineageService:
    def __init__(self, lineage_repo: ArtifactLineageRepository):
        self.lineage_repo = lineage_repo

    def link_artifacts(
        self, source_id: str, target_id: str, relationship_type: str
    ) -> ArtifactLineage:
        link = ArtifactLineage(
            id=f"lin_{uuid.uuid4().hex}",
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            created_at=datetime.utcnow(),
        )
        return self.lineage_repo.save(link)


class ArtifactReuseService:
    def __init__(self, reuse_repo: ReuseRepository):
        self.reuse_repo = reuse_repo

    def evaluate_reuse(self, target_id: str, input_hash: str) -> ReuseEvaluation:
        # Mock reuse logic: Check if input_hash has been evaluated
        evaluation = ReuseEvaluation(
            id=f"reuse_{uuid.uuid4().hex}",
            target_artifact_id=target_id,
            input_hash=input_hash,
            is_reusable=True,
            confidence_score=99.5,
            reason="Exact hash match",
            evaluated_at=datetime.utcnow(),
        )
        return self.reuse_repo.save(evaluation)


class EvidencePackageService:
    def __init__(self, evidence_repo: EvidenceRepository, integrity: IntegrityService):
        self.evidence_repo = evidence_repo
        self.integrity = integrity

    def create_package(self, name: str, artifact_ids: List[str]) -> EvidencePackage:
        signature = self.integrity.sign_package(artifact_ids)

        package = EvidencePackage(
            id=f"pkg_{uuid.uuid4().hex}",
            package_name=name,
            artifact_ids=artifact_ids,
            digital_signature=signature,
            created_at=datetime.utcnow(),
        )
        return self.evidence_repo.save(package)
