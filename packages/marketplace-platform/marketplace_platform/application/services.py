import uuid
from typing import Optional
from datetime import datetime
from marketplace_platform.domain.models import (
    MarketplaceAsset, KnowledgeCapabilityMatrix, Certification, AssetRanking,
    MarketplaceAssetCreate, KnowledgeCapabilityMatrixCreate
)
from marketplace_platform.infrastructure.repositories import (
    MarketplaceAssetRepository, KnowledgeCapabilityMatrixRepository,
    CertificationRepository, AssetRankingRepository
)

class KnowledgeCapabilityMatrixService:
    def __init__(self, capability_repo: KnowledgeCapabilityMatrixRepository):
        self.capability_repo = capability_repo
        
    def evaluate_usability(self, asset_id: str, ai_consumer: str) -> bool:
        matrix = self.capability_repo.get_by_asset_id(asset_id)
        if not matrix:
            return False
        # e.g., if ai_consumer == 'ai_coach', check matrix.ai_usability_json.get('ai_coach', False)
        return matrix.ai_usability_json.get(ai_consumer, False)

    def assign_capability(self, asset_id: str, dto: KnowledgeCapabilityMatrixCreate) -> KnowledgeCapabilityMatrix:
        matrix = KnowledgeCapabilityMatrix(
            id=f"kcm_{uuid.uuid4().hex}",
            asset_id=asset_id,
            scope=dto.scope,
            visibility=dto.visibility,
            sensitivity=dto.sensitivity,
            retention_days=dto.retention_days,
            purge_rules_json=dto.purge_rules_json,
            promotion_eligible_scopes=dto.promotion_eligible_scopes,
            explainability_level=dto.explainability_level,
            ai_usability_json=dto.ai_usability_json,
            updated_at=datetime.utcnow()
        )
        return self.capability_repo.save(matrix)


class MarketplaceService:
    def __init__(
        self, 
        asset_repo: MarketplaceAssetRepository,
        capability_svc: KnowledgeCapabilityMatrixService,
        ranking_repo: AssetRankingRepository
    ):
        self.asset_repo = asset_repo
        self.capability_svc = capability_svc
        self.ranking_repo = ranking_repo

    def publish_asset(self, dto: MarketplaceAssetCreate) -> MarketplaceAsset:
        asset = MarketplaceAsset(
            id=f"ast_{uuid.uuid4().hex}",
            asset_type=dto.asset_type,
            title=dto.title,
            description=dto.description,
            publisher_id=dto.publisher_id,
            version=dto.version,
            status="PUBLISHED",
            categories=dto.categories,
            tags=dto.tags,
            localization=dto.localization,
            content_json=dto.content_json,
            dependencies_json=dto.dependencies_json,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        saved_asset = self.asset_repo.save(asset)
        
        # Attach Governance Capability
        self.capability_svc.assign_capability(saved_asset.id, dto.capability_matrix)
        
        # Initialize Ranking
        ranking = AssetRanking(
            id=f"rnk_{uuid.uuid4().hex}",
            asset_id=saved_asset.id,
            financial_impact_score=0.0,
            completion_rate=0.0,
            roi_score=0.0,
            user_satisfaction=0.0,
            confidence_score=0.0,
            risk_score=0.0,
            ai_recommendation_frequency=0,
            simulation_success_rate=0.0,
            decision_success_rate=0.0,
            overall_quality_score=0.0,
            last_calculated=datetime.utcnow()
        )
        self.ranking_repo.save(ranking)
        
        return self.asset_repo.get_by_id(saved_asset.id)


class RankingService:
    def __init__(self, ranking_repo: AssetRankingRepository):
        self.ranking_repo = ranking_repo
        
    def calculate_overall_quality(self, asset_id: str) -> Optional[AssetRanking]:
        ranking = self.ranking_repo.get_by_asset_id(asset_id)
        if not ranking:
            return None
            
        # Simplified arbitrary weightings for the marketplace ranking
        quality = (
            (ranking.roi_score * 0.3) +
            (ranking.user_satisfaction * 0.2) +
            (ranking.completion_rate * 0.2) +
            (ranking.decision_success_rate * 0.3)
        )
        ranking.overall_quality_score = min(quality, 100.0)
        ranking.last_calculated = datetime.utcnow()
        return self.ranking_repo.save(ranking)


class CertificationService:
    def __init__(self, cert_repo: CertificationRepository):
        self.cert_repo = cert_repo
        
    def grant_certification(self, asset_id: str, certifier_id: str, tier: str) -> Certification:
        cert = Certification(
            id=f"cert_{uuid.uuid4().hex}",
            asset_id=asset_id,
            status="APPROVED",
            certifier_id=certifier_id,
            certification_tier=tier,
            compliance_metadata_json={"audit": "passed"},
            security_metadata_json={"vulnerability_scan": "passed"},
            granted_at=datetime.utcnow()
        )
        return self.cert_repo.save(cert)


class GovernanceService:
    def __init__(self, asset_repo: MarketplaceAssetRepository):
        self.asset_repo = asset_repo
        
    def deprecate_asset(self, asset_id: str, reason: str) -> MarketplaceAsset:
        asset = self.asset_repo.get_by_id(asset_id)
        if asset:
            asset.status = "DEPRECATED"
            asset.updated_at = datetime.utcnow()
            return self.asset_repo.save(asset)
        raise ValueError("Asset not found")
