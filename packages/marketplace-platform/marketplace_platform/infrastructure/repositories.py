from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_

from marketplace_platform.infrastructure.database import (
    MarketplaceAssetModel, KnowledgeCapabilityMatrixModel,
    CertificationModel, AssetRankingModel
)
from marketplace_platform.domain.models import (
    MarketplaceAsset, KnowledgeCapabilityMatrix, Certification, AssetRanking
)

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

class MarketplaceAssetRepository(BaseRepository):
    def get_by_id(self, asset_id: str) -> Optional[MarketplaceAsset]:
        result = self.session.execute(
            select(MarketplaceAssetModel).where(MarketplaceAssetModel.id == asset_id)
        ).scalar_one_or_none()
        return MarketplaceAsset.model_validate(result) if result else None

    def list_assets(self, asset_type: Optional[str] = None, status: str = "PUBLISHED", limit: int = 50) -> List[MarketplaceAsset]:
        query = select(MarketplaceAssetModel).where(MarketplaceAssetModel.status == status)
        if asset_type:
            query = query.where(MarketplaceAssetModel.asset_type == asset_type)
        
        results = self.session.execute(query.limit(limit)).scalars().all()
        return [MarketplaceAsset.model_validate(r) for r in results]

    def save(self, domain: MarketplaceAsset) -> MarketplaceAsset:
        model = self.session.execute(
            select(MarketplaceAssetModel).where(MarketplaceAssetModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            # We don't save nested models via the dictionary directly in this simple setup
            # We assume relations are saved by their respective repos or we map them here
            dump = domain.model_dump(exclude={"capability_matrix", "certification", "ranking"})
            model = MarketplaceAssetModel(**dump)
            self.session.add(model)
        else:
            dump = domain.model_dump(exclude={"capability_matrix", "certification", "ranking"})
            for key, value in dump.items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return MarketplaceAsset.model_validate(model)


class KnowledgeCapabilityMatrixRepository(BaseRepository):
    def get_by_asset_id(self, asset_id: str) -> Optional[KnowledgeCapabilityMatrix]:
        result = self.session.execute(
            select(KnowledgeCapabilityMatrixModel).where(KnowledgeCapabilityMatrixModel.asset_id == asset_id)
        ).scalar_one_or_none()
        return KnowledgeCapabilityMatrix.model_validate(result) if result else None

    def save(self, domain: KnowledgeCapabilityMatrix) -> KnowledgeCapabilityMatrix:
        model = self.session.execute(
            select(KnowledgeCapabilityMatrixModel).where(KnowledgeCapabilityMatrixModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = KnowledgeCapabilityMatrixModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return KnowledgeCapabilityMatrix.model_validate(model)


class CertificationRepository(BaseRepository):
    def get_by_asset_id(self, asset_id: str) -> Optional[Certification]:
        result = self.session.execute(
            select(CertificationModel).where(CertificationModel.asset_id == asset_id)
        ).scalar_one_or_none()
        return Certification.model_validate(result) if result else None

    def save(self, domain: Certification) -> Certification:
        model = self.session.execute(
            select(CertificationModel).where(CertificationModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = CertificationModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return Certification.model_validate(model)


class AssetRankingRepository(BaseRepository):
    def get_by_asset_id(self, asset_id: str) -> Optional[AssetRanking]:
        result = self.session.execute(
            select(AssetRankingModel).where(AssetRankingModel.asset_id == asset_id)
        ).scalar_one_or_none()
        return AssetRanking.model_validate(result) if result else None
        
    def get_top_assets(self, limit: int = 10) -> List[AssetRanking]:
        results = self.session.execute(
            select(AssetRankingModel).order_by(AssetRankingModel.overall_quality_score.desc()).limit(limit)
        ).scalars().all()
        return [AssetRanking.model_validate(r) for r in results]

    def save(self, domain: AssetRanking) -> AssetRanking:
        model = self.session.execute(
            select(AssetRankingModel).where(AssetRankingModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = AssetRankingModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return AssetRanking.model_validate(model)
