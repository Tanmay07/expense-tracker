from unittest.mock import MagicMock
from decision_intelligence.application.services import OpportunityCostService
from decision_intelligence.domain.models import DecisionCandidate, StrategyType
from decision_intelligence.infrastructure.repositories import CandidateRepository


def test_opportunity_cost():
    mock_repo = MagicMock(spec=CandidateRepository)

    candidate = DecisionCandidate(
        user_id="user_123",
        title="Save Money",
        strategy=StrategyType.CONSERVATIVE,
        proposed_actions=[{"type": "save", "amount": 1000}],
    )

    mock_repo.get_by_id.return_value = candidate
    mock_repo.save.side_effect = lambda x: x

    service = OpportunityCostService(mock_repo)
    updated = service.calculate_cost(candidate.id)

    assert updated.opportunity_cost is not None
    # 1000 * 1.05^10 ~ 1628.89
    assert round(updated.opportunity_cost.future_value, 2) == 1628.89
