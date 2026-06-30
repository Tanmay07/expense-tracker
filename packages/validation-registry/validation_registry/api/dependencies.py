from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from validation_registry.infrastructure.database import SessionLocal
from validation_registry.infrastructure.repositories import (
    ArtifactRepository, ArtifactLineageRepository, EvidenceRepository, ReuseRepository
)
from validation_registry.application.services import (
    ArtifactRegistryService, ArtifactStorageService, IntegrityService,
    ArtifactLineageService, ArtifactReuseService, EvidencePackageService
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_artifact_repo(db: Session = Depends(get_db)) -> ArtifactRepository:
    return ArtifactRepository(db)

def get_lineage_repo(db: Session = Depends(get_db)) -> ArtifactLineageRepository:
    return ArtifactLineageRepository(db)

def get_evidence_repo(db: Session = Depends(get_db)) -> EvidenceRepository:
    return EvidenceRepository(db)

def get_reuse_repo(db: Session = Depends(get_db)) -> ReuseRepository:
    return ReuseRepository(db)

# Services

def get_storage_service() -> ArtifactStorageService:
    return ArtifactStorageService()

def get_integrity_service() -> IntegrityService:
    return IntegrityService()

def get_registry_service(
    repo: ArtifactRepository = Depends(get_artifact_repo),
    storage: ArtifactStorageService = Depends(get_storage_service),
    integrity: IntegrityService = Depends(get_integrity_service)
) -> ArtifactRegistryService:
    return ArtifactRegistryService(repo, storage, integrity)

def get_lineage_service(repo: ArtifactLineageRepository = Depends(get_lineage_repo)) -> ArtifactLineageService:
    return ArtifactLineageService(repo)

def get_reuse_service(repo: ReuseRepository = Depends(get_reuse_repo)) -> ArtifactReuseService:
    return ArtifactReuseService(repo)

def get_evidence_service(
    repo: EvidenceRepository = Depends(get_evidence_repo),
    integrity: IntegrityService = Depends(get_integrity_service)
) -> EvidencePackageService:
    return EvidencePackageService(repo, integrity)
