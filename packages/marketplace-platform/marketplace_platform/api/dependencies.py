from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from marketplace_platform.infrastructure.database import SessionLocal
from marketplace_platform.infrastructure.repositories import (
    MarketplaceAssetRepository, KnowledgeCapabilityMatrixRepository,
    CertificationRepository, AssetRankingRepository
)
from marketplace_platform.application.services import (
    MarketplaceService, KnowledgeCapabilityMatrixService, GovernanceService,
    RankingService, CertificationService
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_asset_repo(db: Session = Depends(get_db)) -> MarketplaceAssetRepository:
    return MarketplaceAssetRepository(db)

def get_capability_repo(db: Session = Depends(get_db)) -> KnowledgeCapabilityMatrixRepository:
    return KnowledgeCapabilityMatrixRepository(db)

def get_certification_repo(db: Session = Depends(get_db)) -> CertificationRepository:
    return CertificationRepository(db)

def get_ranking_repo(db: Session = Depends(get_db)) -> AssetRankingRepository:
    return AssetRankingRepository(db)

def get_capability_service(repo: KnowledgeCapabilityMatrixRepository = Depends(get_capability_repo)) -> KnowledgeCapabilityMatrixService:
    return KnowledgeCapabilityMatrixService(repo)

def get_marketplace_service(
    asset_repo: MarketplaceAssetRepository = Depends(get_asset_repo),
    capability_svc: KnowledgeCapabilityMatrixService = Depends(get_capability_service),
    ranking_repo: AssetRankingRepository = Depends(get_ranking_repo)
) -> MarketplaceService:
    return MarketplaceService(asset_repo, capability_svc, ranking_repo)

def get_governance_service(asset_repo: MarketplaceAssetRepository = Depends(get_asset_repo)) -> GovernanceService:
    return GovernanceService(asset_repo)

def get_ranking_service(ranking_repo: AssetRankingRepository = Depends(get_ranking_repo)) -> RankingService:
    return RankingService(ranking_repo)

def get_certification_service(cert_repo: CertificationRepository = Depends(get_certification_repo)) -> CertificationService:
    return CertificationService(cert_repo)
