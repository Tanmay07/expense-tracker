from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional, Any, Dict
from .database import (
    DecisionMemoryModel, PatternModel, PersonalizationModel, PolicyCacheModel,
    PredictionModel, FinancialDNAModel, BehaviorModel, LearningModel, ReplayModel
)
from ..domain.models import (
    DecisionMemoryResponse, PatternResponse, PersonalizationResponse, PolicyCacheResponse,
    PredictionResponse, FinancialDNAResponse, BehaviorResponse, LearningResponse, ReplayResponse
)
import uuid

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class DecisionMemoryRepository(BaseRepository):
    def create(self, memory_data: dict) -> DecisionMemoryResponse:
        record = DecisionMemoryModel(
            id=str(uuid.uuid4()),
            **memory_data
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return DecisionMemoryResponse.model_validate(record)

    def get_by_decision_id(self, decision_id: str) -> Optional[DecisionMemoryResponse]:
        record = self.db.query(DecisionMemoryModel).filter(DecisionMemoryModel.decision_id == decision_id).first()
        if record:
            return DecisionMemoryResponse.model_validate(record)
        return None

    def list_by_user(self, user_id: str) -> List[DecisionMemoryResponse]:
        records = self.db.query(DecisionMemoryModel).filter(DecisionMemoryModel.user_id == user_id).all()
        return [DecisionMemoryResponse.model_validate(r) for r in records]

class PatternRepository(BaseRepository):
    def create(self, pattern_data: dict) -> PatternResponse:
        record = PatternModel(id=str(uuid.uuid4()), **pattern_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return PatternResponse.model_validate(record)

    def list_by_user(self, user_id: str) -> List[PatternResponse]:
        records = self.db.query(PatternModel).filter(PatternModel.user_id == user_id).all()
        return [PatternResponse.model_validate(r) for r in records]

class PersonalizationRepository(BaseRepository):
    def upsert(self, user_id: str, personalization_data: dict) -> PersonalizationResponse:
        record = self.db.query(PersonalizationModel).filter(PersonalizationModel.user_id == user_id).first()
        if record:
            for k, v in personalization_data.items():
                setattr(record, k, v)
        else:
            record = PersonalizationModel(id=str(uuid.uuid4()), user_id=user_id, **personalization_data)
            self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return PersonalizationResponse.model_validate(record)

    def get_by_user(self, user_id: str) -> Optional[PersonalizationResponse]:
        record = self.db.query(PersonalizationModel).filter(PersonalizationModel.user_id == user_id).first()
        if record:
            return PersonalizationResponse.model_validate(record)
        return None

class PolicyDecisionCacheRepository(BaseRepository):
    def create(self, cache_data: dict) -> PolicyCacheResponse:
        record = PolicyCacheModel(id=str(uuid.uuid4()), **cache_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return PolicyCacheResponse.model_validate(record)

    def get_valid_cache(self, decision_id: str, policy_version: int) -> Optional[PolicyCacheResponse]:
        record = self.db.query(PolicyCacheModel).filter(
            PolicyCacheModel.decision_id == decision_id,
            PolicyCacheModel.policy_version == policy_version,
            PolicyCacheModel.is_valid == True
        ).first()
        if record:
            return PolicyCacheResponse.model_validate(record)
        return None

    def invalidate(self, decision_id: str):
        records = self.db.query(PolicyCacheModel).filter(PolicyCacheModel.decision_id == decision_id).all()
        for r in records:
            r.is_valid = False
        self.db.commit()

class PredictionRepository(BaseRepository):
    def create(self, prediction_data: dict) -> PredictionResponse:
        record = PredictionModel(id=str(uuid.uuid4()), **prediction_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return PredictionResponse.model_validate(record)

    def get_latest_by_decision(self, decision_id: str) -> Optional[PredictionResponse]:
        record = self.db.query(PredictionModel).filter(PredictionModel.decision_id == decision_id).order_by(PredictionModel.created_at.desc()).first()
        if record:
            return PredictionResponse.model_validate(record)
        return None

class FinancialDNARepository(BaseRepository):
    def upsert(self, user_id: str, dna_data: dict) -> FinancialDNAResponse:
        record = self.db.query(FinancialDNAModel).filter(FinancialDNAModel.user_id == user_id).first()
        if record:
            for k, v in dna_data.items():
                setattr(record, k, v)
        else:
            record = FinancialDNAModel(id=str(uuid.uuid4()), user_id=user_id, **dna_data)
            self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return FinancialDNAResponse.model_validate(record)

    def get_by_user(self, user_id: str) -> Optional[FinancialDNAResponse]:
        record = self.db.query(FinancialDNAModel).filter(FinancialDNAModel.user_id == user_id).first()
        if record:
            return FinancialDNAResponse.model_validate(record)
        return None

class BehaviorRepository(BaseRepository):
    def create(self, behavior_data: dict) -> BehaviorResponse:
        record = BehaviorModel(id=str(uuid.uuid4()), **behavior_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return BehaviorResponse.model_validate(record)

    def list_by_user(self, user_id: str) -> List[BehaviorResponse]:
        records = self.db.query(BehaviorModel).filter(BehaviorModel.user_id == user_id).order_by(BehaviorModel.created_at.desc()).all()
        return [BehaviorResponse.model_validate(r) for r in records]

class LearningRepository(BaseRepository):
    def create(self, learning_data: dict) -> LearningResponse:
        record = LearningModel(id=str(uuid.uuid4()), **learning_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return LearningResponse.model_validate(record)

class ReplayRepository(BaseRepository):
    def create(self, replay_data: dict) -> ReplayResponse:
        record = ReplayModel(id=str(uuid.uuid4()), **replay_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return ReplayResponse.model_validate(record)

    def get_by_session(self, session_id: str) -> Optional[ReplayResponse]:
        record = self.db.query(ReplayModel).filter(ReplayModel.session_id == session_id).first()
        if record:
            return ReplayResponse.model_validate(record)
        return None
