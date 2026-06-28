import pytest
from unittest.mock import MagicMock
from enterprise_compliance.infrastructure.repositories import (
    SuitabilityRepository, RiskProfileRepository, PolicyRepository, DecisionRepository
)
from enterprise_compliance.domain.models import RiskProfile, RiskLevel

@pytest.fixture
def mock_risk_repo():
    repo = MagicMock(spec=RiskProfileRepository)
    profile = RiskProfile(
        user_id="user_123",
        risk_capacity=0.8,
        risk_tolerance=0.7,
        investment_horizon_years=10,
        liquidity_needs=0.2,
        income_stability_score=0.9,
        emergency_fund_ratio=1.5,
        overall_risk_level=RiskLevel.MODERATE
    )
    repo.get_by_user_id.return_value = profile
    return repo

@pytest.fixture
def mock_suitability_repo():
    repo = MagicMock(spec=SuitabilityRepository)
    repo.save.side_effect = lambda x: x
    return repo

@pytest.fixture
def mock_policy_repo():
    repo = MagicMock(spec=PolicyRepository)
    repo.save.side_effect = lambda x: x
    return repo

@pytest.fixture
def mock_decision_repo():
    repo = MagicMock(spec=DecisionRepository)
    repo.save.side_effect = lambda x: x
    return repo
