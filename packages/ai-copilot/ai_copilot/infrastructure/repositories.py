from sqlalchemy.orm import Session
from typing import List, Optional, Any

from .database import (
    GoalConversationModel, BehavioralProfileModel, ActionPlanModel, 
    SimulationRequestModel, ProactiveAlertModel, get_db
)
from ..domain.models import (
    GoalConversation, BehavioralProfile, ActionPlan, ActionStep, 
    SimulationRequest, ProactiveAlert
)

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class GoalConversationRepository(BaseRepository):
    def get_by_id(self, conversation_id: str) -> Optional[GoalConversation]:
        record = self.db.query(GoalConversationModel).filter(GoalConversationModel.id == conversation_id).first()
        if record:
            data = record.__dict__.copy()
            data.pop('_sa_instance_state', None)
            return GoalConversation(**data)
        return None

    def save(self, conversation: GoalConversation) -> GoalConversation:
        record = GoalConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            goal_type=conversation.goal_type,
            started_at=conversation.started_at,
            active_mode=conversation.active_mode.value,
            progress=conversation.progress,
            action_history=conversation.action_history
        )
        self.db.merge(record)
        self.db.commit()
        return conversation

class BehaviorRepository(BaseRepository):
    def get_by_user_id(self, user_id: str) -> Optional[BehavioralProfile]:
        record = self.db.query(BehavioralProfileModel).filter(BehavioralProfileModel.user_id == user_id).first()
        if record:
            data = record.__dict__.copy()
            data.pop('_sa_instance_state', None)
            return BehavioralProfile(**data)
        return None
        
    def save(self, profile: BehavioralProfile) -> BehavioralProfile:
        record = BehavioralProfileModel(**profile.model_dump())
        self.db.merge(record)
        self.db.commit()
        return profile

class ActionPlanRepository(BaseRepository):
    def get_by_conversation_id(self, conversation_id: str) -> List[ActionPlan]:
        records = self.db.query(ActionPlanModel).filter(ActionPlanModel.conversation_id == conversation_id).all()
        plans = []
        for r in records:
            data = r.__dict__.copy()
            steps_raw = data.pop('steps', [])
            steps = [ActionStep(**s) for s in steps_raw]
            data.pop('_sa_instance_state', None)
            plans.append(ActionPlan(**data, steps=steps))
        return plans
        
    def save(self, plan: ActionPlan) -> ActionPlan:
        data = plan.model_dump()
        steps = [s.model_dump() for s in plan.steps]
        data['steps'] = steps
        
        record = ActionPlanModel(**data)
        self.db.merge(record)
        self.db.commit()
        return plan

class SimulationRequestRepository(BaseRepository):
    def save(self, req: SimulationRequest) -> SimulationRequest:
        record = SimulationRequestModel(**req.model_dump())
        self.db.merge(record)
        self.db.commit()
        return req
