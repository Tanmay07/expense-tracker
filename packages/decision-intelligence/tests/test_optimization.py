from unittest.mock import MagicMock
from decision_intelligence.application.services import OptimizationService
from decision_intelligence.infrastructure.repositories import CandidateRepository


def test_generate_candidates():
    mock_repo = MagicMock(spec=CandidateRepository)
    mock_repo.save.side_effect = lambda x: x

    service = OptimizationService(mock_repo)
    candidates = service.generate_candidates("user_123", {"debt": 5000, "cash": 10000})

    assert len(candidates) == 2
    assert candidates[0].strategy == "DEBT_FIRST"
    assert candidates[1].strategy == "LIQUIDITY_FIRST"
    assert mock_repo.save.call_count == 2
