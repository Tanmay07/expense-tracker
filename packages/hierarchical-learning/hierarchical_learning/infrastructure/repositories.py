from typing import List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_

from hierarchical_learning.infrastructure.database import (
    GlobalLearningModel,
    RegionalLearningModel,
    HouseholdLearningModel,
    HouseholdConsensusModel,
    PersonalLearningModel,
    KnowledgePromotionModel,
    ConsentProfileModel
)
from hierarchical_learning.domain.models import (
    GlobalLearning,
    RegionalLearning,
    HouseholdLearning,
    HouseholdConsensus,
    PersonalLearning,
    KnowledgePromotion,
    ConsentProfile
)

TModel = TypeVar("TModel")
TDomain = TypeVar("TDomain")

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

class GlobalLearningRepository(BaseRepository):
    def get_by_topic(self, topic: str) -> Optional[GlobalLearning]:
        result = self.session.execute(
            select(GlobalLearningModel).where(GlobalLearningModel.topic == topic)
        ).scalar_one_or_none()
        return GlobalLearning.model_validate(result) if result else None

    def save(self, domain: GlobalLearning) -> GlobalLearning:
        model = self.session.execute(
            select(GlobalLearningModel).where(GlobalLearningModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = GlobalLearningModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return GlobalLearning.model_validate(model)

class RegionalLearningRepository(BaseRepository):
    def get_by_region_and_topic(self, region_id: str, topic: str) -> Optional[RegionalLearning]:
        result = self.session.execute(
            select(RegionalLearningModel).where(
                and_(RegionalLearningModel.region_id == region_id, RegionalLearningModel.topic == topic)
            )
        ).scalar_one_or_none()
        return RegionalLearning.model_validate(result) if result else None

    def save(self, domain: RegionalLearning) -> RegionalLearning:
        model = self.session.execute(
            select(RegionalLearningModel).where(RegionalLearningModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = RegionalLearningModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return RegionalLearning.model_validate(model)

class HouseholdLearningRepository(BaseRepository):
    def get_by_household_and_topic(self, household_id: str, topic: str) -> Optional[HouseholdLearning]:
        result = self.session.execute(
            select(HouseholdLearningModel).where(
                and_(HouseholdLearningModel.household_id == household_id, HouseholdLearningModel.topic == topic)
            )
        ).scalar_one_or_none()
        return HouseholdLearning.model_validate(result) if result else None

    def save(self, domain: HouseholdLearning) -> HouseholdLearning:
        model = self.session.execute(
            select(HouseholdLearningModel).where(HouseholdLearningModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = HouseholdLearningModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return HouseholdLearning.model_validate(model)

class HouseholdConsensusRepository(BaseRepository):
    def get_by_household_and_topic(self, household_id: str, topic: str) -> Optional[HouseholdConsensus]:
        result = self.session.execute(
            select(HouseholdConsensusModel).where(
                and_(HouseholdConsensusModel.household_id == household_id, HouseholdConsensusModel.conflict_topic == topic)
            )
        ).scalar_one_or_none()
        return HouseholdConsensus.model_validate(result) if result else None

    def save(self, domain: HouseholdConsensus) -> HouseholdConsensus:
        model = self.session.execute(
            select(HouseholdConsensusModel).where(HouseholdConsensusModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = HouseholdConsensusModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return HouseholdConsensus.model_validate(model)

class PersonalLearningRepository(BaseRepository):
    def get_by_user_and_topic(self, user_id: str, topic: str) -> Optional[PersonalLearning]:
        result = self.session.execute(
            select(PersonalLearningModel).where(
                and_(PersonalLearningModel.user_id == user_id, PersonalLearningModel.topic == topic)
            )
        ).scalar_one_or_none()
        return PersonalLearning.model_validate(result) if result else None
        
    def find_similar_behavior(self, embedding: List[float], limit: int = 5) -> List[PersonalLearning]:
        # Uses pgvector L2 distance operator (<->)
        results = self.session.execute(
            select(PersonalLearningModel)
            .order_by(PersonalLearningModel.semantic_embedding.l2_distance(embedding))
            .limit(limit)
        ).scalars().all()
        return [PersonalLearning.model_validate(r) for r in results]

    def save(self, domain: PersonalLearning) -> PersonalLearning:
        model = self.session.execute(
            select(PersonalLearningModel).where(PersonalLearningModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = PersonalLearningModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return PersonalLearning.model_validate(model)

class KnowledgePromotionRepository(BaseRepository):
    def get_pending_promotions(self, target_scope: str) -> List[KnowledgePromotion]:
        results = self.session.execute(
            select(KnowledgePromotionModel).where(
                and_(
                    KnowledgePromotionModel.target_scope == target_scope,
                    KnowledgePromotionModel.promotion_status.in_(["OBSERVED", "CANDIDATE"])
                )
            )
        ).scalars().all()
        return [KnowledgePromotion.model_validate(r) for r in results]

    def save(self, domain: KnowledgePromotion) -> KnowledgePromotion:
        model = self.session.execute(
            select(KnowledgePromotionModel).where(KnowledgePromotionModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = KnowledgePromotionModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return KnowledgePromotion.model_validate(model)

class ConsentRepository(BaseRepository):
    def get_profile(self, user_id: str) -> Optional[ConsentProfile]:
        result = self.session.execute(
            select(ConsentProfileModel).where(ConsentProfileModel.user_id == user_id)
        ).scalar_one_or_none()
        return ConsentProfile.model_validate(result) if result else None

    def save(self, domain: ConsentProfile) -> ConsentProfile:
        model = self.session.execute(
            select(ConsentProfileModel).where(ConsentProfileModel.id == domain.id)
        ).scalar_one_or_none()
        
        if not model:
            model = ConsentProfileModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
                
        self.session.commit()
        self.session.refresh(model)
        return ConsentProfile.model_validate(model)
