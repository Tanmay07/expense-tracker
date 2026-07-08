from mission_control.application.services import PriorityService
from mission_control.domain.models import Mission, MissionPriority, MissionExplanation


def _create_mock_mission(title: str, urgency: float, impact: float) -> Mission:
    priority = MissionPriority(
        level="MEDIUM",
        urgency_score=urgency,
        financial_impact_score=impact,
        confidence=0.9,
        business_impact="None",
    )
    explanation = MissionExplanation(
        summary="Test",
        supporting_metrics={},
        timeline_events=[],
        policies_evaluated=[],
        expected_financial_benefit=0.0,
    )
    return Mission(
        user_id="user_1",
        title=title,
        type="TODAYS_TASKS",
        priority=priority,
        explanation=explanation,
    )


def test_mission_conflict_resolution():
    service = PriorityService()

    # Create two missions with same title but different urgency
    m1 = _create_mock_mission("Duplicate Mission", 0.5, 0.5)
    m2 = _create_mock_mission("Duplicate Mission", 0.9, 0.5)

    resolved = service.resolve_conflicts([m1, m2])

    # Should merge down to 1 mission
    assert len(resolved) == 1
    # Should keep the one with higher urgency
    assert resolved[0].priority.urgency_score == 0.9


def test_mission_ranking():
    service = PriorityService()

    m1 = _create_mock_mission("Low Urgency", 0.2, 0.5)
    m2 = _create_mock_mission("High Urgency", 0.9, 0.5)
    m3 = _create_mock_mission("Mid Urgency", 0.5, 0.9)

    ranked = service.rank_missions([m1, m2, m3])

    assert ranked[0].title == "High Urgency"
    assert ranked[1].title == "Mid Urgency"
    assert ranked[2].title == "Low Urgency"
