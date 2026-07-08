from unittest.mock import MagicMock
from ai_copilot.application.orchestration import DecisionIntelligenceService
from ai_copilot.application.services import ActionPlanService
from ai_copilot.infrastructure.repositories import ActionPlanRepository


def test_action_plan_generation():
    mock_repo = MagicMock(spec=ActionPlanRepository)
    mock_repo.save.side_effect = lambda x: x

    decision_service = DecisionIntelligenceService()
    service = ActionPlanService(mock_repo, decision_service)

    plan = service.generate_plan("user_123", "conv_123", "Build Emergency Fund")

    assert plan.status == "APPROVED"
    assert plan.priority == "HIGH"
    assert len(plan.steps) == 2
    mock_repo.save.assert_called_once()
