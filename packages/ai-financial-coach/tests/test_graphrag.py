from ai_financial_coach.application.orchestration import ContextService
from ai_financial_coach.domain.models import ContextFrame

def test_build_context():
    service = ContextService()
    context = service.build_context("user_123", "dummy query")
    
    assert isinstance(context, ContextFrame)
    assert "monthly_spend" in context.metrics
    assert len(context.active_policies) == 1
    assert context.active_policies[0]["name"] == "Max Crypto"
