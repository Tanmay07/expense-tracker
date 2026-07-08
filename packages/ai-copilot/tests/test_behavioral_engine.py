from unittest.mock import MagicMock, patch
from ai_copilot.application.services import CopilotService
from ai_copilot.application.orchestration import AgentCoordinatorService
from ai_copilot.infrastructure.repositories import (
    GoalConversationRepository,
    BehaviorRepository,
)
from ai_copilot.domain.models import CopilotMode


@patch("ai_copilot.application.orchestration.completion")
def test_copilot_routing(mock_completion):
    mock_choice = MagicMock()
    mock_choice.message.content = "Here is your debt reduction plan."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_completion.return_value = mock_response

    mock_conv_repo = MagicMock(spec=GoalConversationRepository)
    mock_conv_repo.get_by_id.return_value = None
    mock_conv_repo.save.side_effect = lambda x: x

    mock_beh_repo = MagicMock(spec=BehaviorRepository)
    mock_beh_repo.get_by_user_id.return_value = None

    coordinator = AgentCoordinatorService()
    service = CopilotService(mock_conv_repo, mock_beh_repo, coordinator)

    response = service.handle_message(
        "user_1", "conv_1", "How do I pay off my car?", CopilotMode.DEBT_COACH
    )

    assert response == "Here is your debt reduction plan."
    mock_conv_repo.save.assert_called()
