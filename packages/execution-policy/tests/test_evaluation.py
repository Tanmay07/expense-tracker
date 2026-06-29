from unittest.mock import MagicMock
from execution_policy.application.services import PolicyEvaluationService
from execution_policy.infrastructure.repositories import PolicyRepository, EvaluationRepository
from execution_policy.domain.models import ExecutionPolicy, PolicyContext, RuleAST, RuleOperator, EvaluationOutcome, PolicyCategory

def test_evaluate_policy_match():
    mock_policy_repo = MagicMock(spec=PolicyRepository)
    mock_eval_repo = MagicMock(spec=EvaluationRepository)
    
    mock_eval_repo.save.side_effect = lambda x: x
    
    policy = ExecutionPolicy(
        name="High Risk Auto Deny",
        description="Deny if fully automated and high risk",
        category=PolicyCategory.RISK,
        outcome_if_matched=EvaluationOutcome.DENY,
        rule_ast=RuleAST(
            operator=RuleOperator.AND,
            conditions=[
                RuleAST(operator=RuleOperator.EQ, field="capability_metadata.automation_level", value="FULLY_AUTOMATED"),
                RuleAST(operator=RuleOperator.EQ, field="capability_metadata.risk_level", value="HIGH")
            ]
        )
    )
    
    mock_policy_repo.list_active.return_value = [policy]
    
    service = PolicyEvaluationService(mock_policy_repo, mock_eval_repo)
    
    context = PolicyContext(
        request_id="req_123",
        decision_metadata={},
        capability_metadata={"automation_level": "FULLY_AUTOMATED", "risk_level": "HIGH"},
        user_metadata={},
        risk_profile={}
    )
    
    result = service.evaluate(context)
    
    assert result.outcome == EvaluationOutcome.DENY
    assert result.explanation.triggering_policy_id == policy.id
    
def test_evaluate_default_allow():
    mock_policy_repo = MagicMock(spec=PolicyRepository)
    mock_eval_repo = MagicMock(spec=EvaluationRepository)
    
    mock_eval_repo.save.side_effect = lambda x: x
    mock_policy_repo.list_active.return_value = []
    
    service = PolicyEvaluationService(mock_policy_repo, mock_eval_repo)
    
    context = PolicyContext(
        request_id="req_456",
        decision_metadata={},
        capability_metadata={},
        user_metadata={},
        risk_profile={}
    )
    
    result = service.evaluate(context)
    
    # If no policies match, default is ALLOW
    assert result.outcome == EvaluationOutcome.ALLOW
    assert result.explanation.triggering_policy_name == "Default Allow"
