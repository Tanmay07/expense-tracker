from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import (
    GoalConversationRepository, BehaviorRepository, 
    ActionPlanRepository, SimulationRequestRepository
)
from ..application.orchestration import AgentCoordinatorService, DecisionIntelligenceService
from ..application.services import CopilotService, ActionPlanService, SimulationRequestService

def get_conversation_repo(db: Session = Depends(get_db)):
    return GoalConversationRepository(db)
    
def get_behavior_repo(db: Session = Depends(get_db)):
    return BehaviorRepository(db)

def get_action_plan_repo(db: Session = Depends(get_db)):
    return ActionPlanRepository(db)

def get_simulation_repo(db: Session = Depends(get_db)):
    return SimulationRequestRepository(db)

def get_copilot_service(
    conv_repo: GoalConversationRepository = Depends(get_conversation_repo),
    beh_repo: BehaviorRepository = Depends(get_behavior_repo)
) -> CopilotService:
    coordinator = AgentCoordinatorService()
    return CopilotService(conv_repo, beh_repo, coordinator)

def get_action_plan_service(
    repo: ActionPlanRepository = Depends(get_action_plan_repo)
) -> ActionPlanService:
    decision = DecisionIntelligenceService()
    return ActionPlanService(repo, decision)
    
def get_simulation_service(
    repo: SimulationRequestRepository = Depends(get_simulation_repo)
) -> SimulationRequestService:
    return SimulationRequestService(repo)
