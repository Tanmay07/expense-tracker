from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from marketplace_platform.domain.models import (
    MarketplaceAsset, MarketplaceAssetCreate, Certification
)
from marketplace_platform.application.services import (
    MarketplaceService, KnowledgeCapabilityMatrixService, GovernanceService,
    CertificationService
)
from marketplace_platform.api.dependencies import (
    get_marketplace_service, get_capability_service, get_governance_service,
    get_certification_service, get_asset_repo
)
from marketplace_platform.infrastructure.repositories import MarketplaceAssetRepository

router = APIRouter()

@router.post("/assets")
def publish_asset(
    dto: MarketplaceAssetCreate,
    svc: MarketplaceService = Depends(get_marketplace_service)
) -> MarketplaceAsset:
    return svc.publish_asset(dto)

@router.get("/assets", response_model=List[MarketplaceAsset])
def list_assets(
    asset_type: Optional[str] = None,
    repo: MarketplaceAssetRepository = Depends(get_asset_repo)
) -> List[MarketplaceAsset]:
    return repo.list_assets(asset_type=asset_type)

@router.get("/assets/{asset_id}")
def get_asset(
    asset_id: str,
    repo: MarketplaceAssetRepository = Depends(get_asset_repo)
) -> MarketplaceAsset:
    asset = repo.get_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/assets/{asset_id}/deprecate")
def deprecate_asset(
    asset_id: str,
    reason: str,
    svc: GovernanceService = Depends(get_governance_service)
) -> MarketplaceAsset:
    try:
        return svc.deprecate_asset(asset_id, reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/assets/{asset_id}/usability")
def check_ai_usability(
    asset_id: str,
    ai_consumer: str,
    svc: KnowledgeCapabilityMatrixService = Depends(get_capability_service)
) -> bool:
    return svc.evaluate_usability(asset_id, ai_consumer)

@router.post("/assets/{asset_id}/certify")
def grant_certification(
    asset_id: str,
    certifier_id: str,
    tier: str,
    svc: CertificationService = Depends(get_certification_service)
) -> Certification:
    return svc.grant_certification(asset_id, certifier_id, tier)
