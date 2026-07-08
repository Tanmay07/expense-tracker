from enterprise_compliance.application.services import SuitabilityService
import pytest


def test_evaluate_suitability_success(mock_suitability_repo, mock_risk_repo):
    service = SuitabilityService(mock_suitability_repo, mock_risk_repo)
    result = service.evaluate_suitability("user_123", {"investment_amount": 10000})

    assert result.user_id == "user_123"
    assert result.suitability_score == 85.0
    assert result.confidence_score == 0.95
    mock_risk_repo.get_by_user_id.assert_called_once_with("user_123")
    mock_suitability_repo.save.assert_called_once()


def test_evaluate_suitability_no_profile(mock_suitability_repo, mock_risk_repo):
    mock_risk_repo.get_by_user_id.return_value = None
    service = SuitabilityService(mock_suitability_repo, mock_risk_repo)

    with pytest.raises(ValueError, match="User Risk Profile not found"):
        service.evaluate_suitability("user_unknown", {})
