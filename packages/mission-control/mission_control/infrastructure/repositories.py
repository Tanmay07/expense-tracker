from sqlalchemy.orm import Session
from typing import List, Optional

from .database import MissionModel, OpportunityModel, RiskModel, MissionStatusEnum
from ..domain.models import Mission, Opportunity, Risk, MissionPriority, MissionExplanation, ActionTask

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class MissionRepository(BaseRepository):
    def get_by_id(self, mission_id: str) -> Optional[Mission]:
        record = self.db.query(MissionModel).filter(MissionModel.id == mission_id).first()
        if not record:
            return None
            
        priority = MissionPriority(
            level=record.priority_level,
            urgency_score=record.urgency_score,
            financial_impact_score=record.financial_impact_score,
            confidence=record.confidence,
            business_impact=record.business_impact
        )
        explanation = MissionExplanation(**record.explanation)
        actions = [ActionTask(**a) for a in record.actions]
        
        return Mission(
            id=record.id,
            user_id=record.user_id,
            title=record.title,
            type=record.type,
            status=record.status,
            priority=priority,
            explanation=explanation,
            actions=actions,
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    def get_active_by_user(self, user_id: str) -> List[Mission]:
        records = self.db.query(MissionModel).filter(
            MissionModel.user_id == user_id,
            MissionModel.status.in_([MissionStatusEnum.CREATED, MissionStatusEnum.UPDATED])
        ).order_by(MissionModel.urgency_score.desc()).all()
        # Full mapper skipped for brevity in get_active...
        missions = []
        for r in records:
            missions.append(self.get_by_id(r.id))
        return missions

    def save(self, mission: Mission) -> Mission:
        record = MissionModel(
            id=mission.id,
            user_id=mission.user_id,
            title=mission.title,
            type=mission.type.value,
            status=mission.status.value,
            priority_level=mission.priority.level,
            urgency_score=mission.priority.urgency_score,
            financial_impact_score=mission.priority.financial_impact_score,
            confidence=mission.priority.confidence,
            business_impact=mission.priority.business_impact,
            explanation=mission.explanation.model_dump(),
            actions=[a.model_dump() for a in mission.actions],
            created_at=mission.created_at,
            updated_at=mission.updated_at
        )
        self.db.merge(record)
        self.db.commit()
        return mission

class OpportunityRepository(BaseRepository):
    def save(self, opp: Opportunity) -> Opportunity:
        record = OpportunityModel(
            id=opp.id,
            user_id=opp.user_id,
            title=opp.title,
            description=opp.description,
            score=opp.score,
            metadata_json=opp.metadata,
            created_at=opp.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return opp
        
class RiskRepository(BaseRepository):
    def save(self, risk: Risk) -> Risk:
        record = RiskModel(
            id=risk.id,
            user_id=risk.user_id,
            title=risk.title,
            severity=risk.severity,
            description=risk.description,
            metadata_json=risk.metadata,
            created_at=risk.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return risk
