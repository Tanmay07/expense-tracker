from mission_control.application.services import MissionGeneratorService
from mission_control.domain.models import Opportunity, Risk

def test_generate_from_opportunity():
    generator = MissionGeneratorService()
    
    opp = Opportunity(
        user_id="user_123",
        title="Test Opportunity",
        description="A good investment",
        score=0.9,
        metadata={}
    )
    
    mission = generator.generate_from_opportunity(opp)
    assert mission.type == "RECOMMENDED_ACTIONS"
    assert mission.priority.financial_impact_score == 0.9
    assert mission.explanation.expected_financial_benefit == 900.0

def test_generate_from_risk():
    generator = MissionGeneratorService()
    
    risk = Risk(
        user_id="user_123",
        title="High Debt",
        severity="HIGH",
        description="Debt is getting out of hand",
        metadata={}
    )
    
    mission = generator.generate_from_risk(risk)
    assert mission.type == "CRITICAL_ALERTS"
    assert mission.priority.level == "HIGH"
    assert mission.priority.urgency_score == 0.9
