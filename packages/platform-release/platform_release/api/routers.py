from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Simple DB dependency
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from platform_release.infrastructure.repositories import ReleaseRepository  # noqa: E402
from platform_release.application.services import (  # noqa: E402
    PlatformBaselineService,
    ContractFreezeService,
    DocumentationFreezeService,
    ReleaseCertificationService,
    PlatformVersioningService,
    MissionReadinessService,
    GovernanceLifecycleService
)

router = APIRouter(prefix="/api/v1/platform", tags=["Platform Release"])

def get_repository(db: Session = Depends(get_db)) -> ReleaseRepository:
    return ReleaseRepository(db)

@router.post("/baseline")
def capture_baseline(version: str, repo: ReleaseRepository = Depends(get_repository)):
    svc = PlatformBaselineService(repo)
    return svc.capture_baseline(version)

@router.post("/contracts/freeze")
def freeze_contracts(version: str, repo: ReleaseRepository = Depends(get_repository)):
    svc = ContractFreezeService(repo)
    return svc.freeze_contracts(version)

@router.post("/documentation/freeze")
def freeze_documentation(version: str, repo: ReleaseRepository = Depends(get_repository)):
    svc = DocumentationFreezeService(repo)
    return svc.freeze_documentation(version)

@router.post("/certification")
def certify_release(version: str, repo: ReleaseRepository = Depends(get_repository)):
    svc = ReleaseCertificationService(repo)
    return svc.certify_release(version)

@router.post("/release")
def generate_release(
    version: str,
    certification_id: str,
    baseline_id: str,
    contract_matrix_id: str,
    doc_index_id: str,
    repo: ReleaseRepository = Depends(get_repository)
):
    svc = PlatformVersioningService(repo)
    return svc.generate_release_manifest(version, certification_id, baseline_id, contract_matrix_id, doc_index_id)

@router.get("/version/{version}")
def get_release_manifest(version: str, repo: ReleaseRepository = Depends(get_repository)):
    manifest = repo.get_release_manifest(version)
    if not manifest:
        raise HTTPException(status_code=404, detail="Version not found")
    return manifest

@router.get("/readiness/{version}")
def check_readiness(version: str, repo: ReleaseRepository = Depends(get_repository)):
    svc = MissionReadinessService(repo)
    return svc.check_readiness(version)

@router.get("/governance/lifecycle")
def get_lifecycle(repo: ReleaseRepository = Depends(get_repository)):
    svc = GovernanceLifecycleService(repo)
    return svc.validate_lifecycle()
