from unittest.mock import MagicMock
from decision_lifecycle.application.services import ExecutionPlannerService
from decision_lifecycle.infrastructure.repositories import ExecutionPlanRepository


def test_execution_plan_generation():
    mock_repo = MagicMock(spec=ExecutionPlanRepository)
    mock_repo.save.side_effect = lambda x: x

    service = ExecutionPlannerService(mock_repo)

    actions = [{"type": "pay_debt", "amount": 5000}, {"type": "open_account"}]

    plan = service.generate_plan("dec_123", actions)

    assert len(plan.steps) == 2
    assert plan.steps[0].required_funds == 5000.0
    assert len(plan.milestones) == 1
    assert plan.estimated_duration_days == 5
