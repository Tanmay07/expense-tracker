from typing import Dict, Any

from ..domain.models import (
    GoalConversation, ActionPlan, ActionStep, SimulationRequest, CopilotMode
)
from ..infrastructure.repositories import (
    GoalConversationRepository, ActionPlanRepository, 
    BehaviorRepository, SimulationRequestRepository
)
from .orchestration import AgentCoordinatorService, DecisionIntelligenceService

class CopilotService:
    def __init__(
        self,
        conversation_repo: GoalConversationRepository,
        behavior_repo: BehaviorRepository,
        coordinator: AgentCoordinatorService
    ):
        self.conversation_repo = conversation_repo
        self.behavior_repo = behavior_repo
        self.coordinator = coordinator

    def handle_message(self, user_id: str, conversation_id: str, message: str, mode: CopilotMode = CopilotMode.DAILY_COACH) -> str:
        conv = self.conversation_repo.get_by_id(conversation_id)
        if not conv:
            conv = GoalConversation(id=conversation_id, user_id=user_id, goal_type="General", active_mode=mode)
            self.conversation_repo.save(conv)
            
        behavior = self.behavior_repo.get_by_user_id(user_id)
        context = {"behavior": behavior.model_dump() if behavior else {}}
        
        response = self.coordinator.coordinate_agents(mode, context, message)
        
        conv.action_history.append(f"User: {message}")
        conv.action_history.append(f"Copilot: {response}")
        self.conversation_repo.save(conv)
        
        return response

class ActionPlanService:
    def __init__(self, plan_repo: ActionPlanRepository, decision_service: DecisionIntelligenceService):
        self.plan_repo = plan_repo
        self.decision_service = decision_service
        
    def generate_plan(self, user_id: str, conversation_id: str, goal: str) -> ActionPlan:
        # Mock generation
        plan = ActionPlan(
            user_id=user_id,
            conversation_id=conversation_id,
            priority="HIGH",
            expected_impact="Goal Achieved",
            steps=[
                ActionStep(description="Analyze current savings", dependencies=[]),
                ActionStep(description="Allocate 10% to emergency fund", dependencies=[])
            ]
        )
        
        eval_result = self.decision_service.evaluate_action_plan(conversation_id, plan)
        if eval_result["is_approved"]:
            plan.status = "APPROVED"
            
        return self.plan_repo.save(plan)

class SimulationRequestService:
    def __init__(self, repo: SimulationRequestRepository):
        self.repo = repo
        
    def request_simulation(self, user_id: str, scenario: str, assumptions: Dict[str, Any]) -> SimulationRequest:
        req = SimulationRequest(
            user_id=user_id,
            scenario_type=scenario,
            assumptions=assumptions
        )
        return self.repo.save(req)
