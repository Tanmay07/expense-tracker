from sqlalchemy.orm import Session
from typing import List, Optional

from .database import (
    RiskProfileModel, CompliancePolicyModel, SuitabilityProfileModel, 
    InvestmentConstraintModel, DecisionRecordModel
)
from ..domain.models import (
    RiskProfile, CompliancePolicy, SuitabilityProfile, 
    InvestmentConstraint, DecisionRecord
)

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class RiskProfileRepository(BaseRepository):
    def get_by_user_id(self, user_id: str) -> Optional[RiskProfile]:
        record = self.db.query(RiskProfileModel).filter(RiskProfileModel.user_id == user_id).first()
        if record:
            return RiskProfile(**record.__dict__)
        return None
        
    def save(self, profile: RiskProfile) -> RiskProfile:
        record = RiskProfileModel(**profile.model_dump())
        self.db.merge(record)
        self.db.commit()
        return profile

class PolicyRepository(BaseRepository):
    def get_active_policies(self) -> List[CompliancePolicy]:
        records = self.db.query(CompliancePolicyModel).filter(CompliancePolicyModel.is_active == True).all()
        return [CompliancePolicy(**r.__dict__) for r in records]

    def save(self, policy: CompliancePolicy) -> CompliancePolicy:
        record = CompliancePolicyModel(**policy.model_dump())
        self.db.merge(record)
        self.db.commit()
        return policy

class SuitabilityRepository(BaseRepository):
    def get_by_user_id(self, user_id: str) -> Optional[SuitabilityProfile]:
        record = self.db.query(SuitabilityProfileModel).filter(SuitabilityProfileModel.user_id == user_id).first()
        if record:
            return SuitabilityProfile(**record.__dict__)
        return None

    def save(self, profile: SuitabilityProfile) -> SuitabilityProfile:
        record = SuitabilityProfileModel(**profile.model_dump())
        self.db.merge(record)
        self.db.commit()
        return profile

class ConstraintRepository(BaseRepository):
    def get_by_user_id(self, user_id: str) -> List[InvestmentConstraint]:
        records = self.db.query(InvestmentConstraintModel).filter(InvestmentConstraintModel.user_id == user_id).all()
        return [InvestmentConstraint(**r.__dict__) for r in records]

    def save(self, constraint: InvestmentConstraint) -> InvestmentConstraint:
        record = InvestmentConstraintModel(**constraint.model_dump())
        self.db.merge(record)
        self.db.commit()
        return constraint

class DecisionRepository(BaseRepository):
    def get_by_context_id(self, context_id: str) -> List[DecisionRecord]:
        records = self.db.query(DecisionRecordModel).filter(DecisionRecordModel.context_id == context_id).all()
        return [DecisionRecord(**r.__dict__) for r in records]

    def save(self, decision: DecisionRecord) -> DecisionRecord:
        record = DecisionRecordModel(**decision.model_dump())
        self.db.merge(record)
        self.db.commit()
        return decision
