from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from validation_registry.domain.models import (
    ArtifactRecord, ArtifactRecordCreate, ArtifactLineage, EvidencePackage, ReuseEvaluation
)
from validation_registry.application.services import (
    ArtifactRegistryService, ArtifactLineageService,
    ArtifactReuseService, EvidencePackageService
)
from validation_registry.api.dependencies import (
    get_registry_service, get_lineage_service, get_reuse_service, get_evidence_service,
    get_artifact_repo, get_lineage_repo
)
from validation_registry.infrastructure.repositories import (
    ArtifactRepository, ArtifactLineageRepository
)
import json

router = APIRouter()

class EvidencePackageCreate(BaseModel):
    name: str
    artifact_ids: List[str]

@router.post("/artifacts", response_model=ArtifactRecord)
async def register_artifact(
    payload_file: UploadFile = File(...),
    metadata: str = Form(...),
    svc: ArtifactRegistryService = Depends(get_registry_service)
):
    try:
        dto = ArtifactRecordCreate.model_validate_json(metadata)
        payload_bytes = await payload_file.read()
        return svc.register_artifact(dto, payload_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/artifacts", response_model=List[ArtifactRecord])
def list_artifacts(
    category: Optional[str] = None,
    repo: ArtifactRepository = Depends(get_artifact_repo)
):
    return repo.list_artifacts(category=category)

@router.get("/artifacts/{artifact_id}", response_model=ArtifactRecord)
def get_artifact(
    artifact_id: str,
    repo: ArtifactRepository = Depends(get_artifact_repo)
):
    record = repo.get_by_id(artifact_id)
    if not record:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return record


@router.post("/artifacts/{artifact_id}/lineage", response_model=ArtifactLineage)
def link_lineage(
    artifact_id: str,
    target_id: str,
    relationship_type: str,
    svc: ArtifactLineageService = Depends(get_lineage_service)
):
    return svc.link_artifacts(artifact_id, target_id, relationship_type)

@router.get("/artifacts/{artifact_id}/lineage", response_model=List[ArtifactLineage])
def get_lineage(
    artifact_id: str,
    repo: ArtifactLineageRepository = Depends(get_lineage_repo)
):
    return repo.get_by_source_id(artifact_id)

@router.post("/reuse/evaluate", response_model=ReuseEvaluation)
def evaluate_reuse(
    target_id: str,
    input_hash: str,
    svc: ArtifactReuseService = Depends(get_reuse_service)
):
    return svc.evaluate_reuse(target_id, input_hash)

@router.post("/evidence", response_model=EvidencePackage)
def create_evidence_package(
    payload: EvidencePackageCreate,
    svc: EvidencePackageService = Depends(get_evidence_service)
):
    return svc.create_package(payload.name, payload.artifact_ids)
