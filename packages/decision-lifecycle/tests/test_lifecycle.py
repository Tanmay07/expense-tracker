import pytest
from unittest.mock import MagicMock
from decision_lifecycle.application.services import DecisionLifecycleService
from decision_lifecycle.domain.models import DecisionLifecycle, LifecycleState
from decision_lifecycle.infrastructure.repositories import LifecycleRepository


def test_lifecycle_initialization():
    mock_repo = MagicMock(spec=LifecycleRepository)
    mock_repo.save.side_effect = lambda x: x

    service = DecisionLifecycleService(mock_repo)
    lifecycle = service.initialize_lifecycle("dec_123")

    assert lifecycle.current_state == LifecycleState.GENERATED
    assert len(lifecycle.state_history) == 1
    assert lifecycle.state_history[0]["state"] == "GENERATED"


def test_valid_state_transition():
    mock_repo = MagicMock(spec=LifecycleRepository)

    lifecycle = DecisionLifecycle(
        decision_id="dec_123", current_state=LifecycleState.GENERATED
    )
    mock_repo.get_by_decision_id.return_value = lifecycle
    mock_repo.save.side_effect = lambda x: x

    service = DecisionLifecycleService(mock_repo)
    updated = service.transition_state("dec_123", LifecycleState.PENDING_REVIEW)

    assert updated.current_state == LifecycleState.PENDING_REVIEW
    assert len(updated.state_history) == 1


def test_invalid_state_transition():
    mock_repo = MagicMock(spec=LifecycleRepository)

    # DRAFT -> COMPLETED is invalid
    lifecycle = DecisionLifecycle(
        decision_id="dec_123", current_state=LifecycleState.DRAFT
    )
    mock_repo.get_by_decision_id.return_value = lifecycle

    service = DecisionLifecycleService(mock_repo)

    with pytest.raises(ValueError, match="Invalid transition"):
        service.transition_state("dec_123", LifecycleState.COMPLETED)
