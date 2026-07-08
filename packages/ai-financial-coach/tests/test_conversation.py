import pytest
from unittest.mock import MagicMock, patch
from ai_financial_coach.application.services import CoachService
from ai_financial_coach.application.orchestration import (
    AgentCoordinatorService,
    ContextService,
    ExplainabilityService,
)
from ai_financial_coach.infrastructure.repositories import ConversationRepository
from ai_financial_coach.domain.models import Role


@pytest.fixture
def mock_conversation_repo():
    repo = MagicMock(spec=ConversationRepository)
    repo.get_by_id.return_value = None
    repo.save.side_effect = lambda x: x
    return repo


@patch("ai_financial_coach.application.agents.completion")
def test_process_message(mock_completion, mock_conversation_repo):
    # Mock litellm response
    mock_choice = MagicMock()
    mock_choice.message.content = "Here is your expense analysis."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_completion.return_value = mock_response

    coordinator = AgentCoordinatorService()
    context_service = ContextService()
    explain_service = ExplainabilityService()

    coach = CoachService(
        mock_conversation_repo, coordinator, context_service, explain_service
    )

    result = coach.process_message(
        conversation_id="conv_123",
        user_id="user_123",
        content="How much did I spend on food?",
    )

    assert result.role == Role.ASSISTANT
    assert result.content == "Here is your expense analysis."
    assert result.explainability_metadata is not None
    assert "metrics_used" in result.explainability_metadata

    mock_conversation_repo.save.assert_called_once()
