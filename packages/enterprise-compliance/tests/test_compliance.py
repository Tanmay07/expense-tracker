from enterprise_compliance.application.services import ComplianceService
from enterprise_compliance.domain.models import CompliancePolicy, PolicyType, PolicySeverity
from enterprise_compliance.domain.models import DecisionStatus

def test_evaluate_transaction_compliant(mock_policy_repo, mock_decision_repo):
    policy = CompliancePolicy(
        name="Maximum Equity Exposure",
        type=PolicyType.ALLOCATION,
        description="Limit",
        severity=PolicySeverity.VIOLATION,
        rule_expression="x < y"
    )
    mock_policy_repo.get_active_policies.return_value = [policy]
    
    service = ComplianceService(mock_policy_repo, mock_decision_repo)
    result = service.evaluate_transaction("user_123", "ctx_123", {"asset_class": "EQUITY"})
    
    assert result.is_compliant is True
    assert len(result.violations) == 0
    mock_decision_repo.save.assert_called_once()

def test_evaluate_transaction_violation(mock_policy_repo, mock_decision_repo):
    policy = CompliancePolicy(
        name="Maximum Crypto Exposure",
        type=PolicyType.ALLOCATION,
        description="Limit Crypto",
        severity=PolicySeverity.VIOLATION,
        rule_expression="x < y"
    )
    mock_policy_repo.get_active_policies.return_value = [policy]
    
    service = ComplianceService(mock_policy_repo, mock_decision_repo)
    result = service.evaluate_transaction("user_123", "ctx_123", {"asset_class": "CRYPTO"})
    
    assert result.is_compliant is False
    assert len(result.violations) == 1
    assert result.violations[0] == policy.id
    mock_decision_repo.save.assert_called_once()
