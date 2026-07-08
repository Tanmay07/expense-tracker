from unittest.mock import MagicMock
from execution_capability.application.services import ApprovalService
from execution_capability.infrastructure.repositories import ApprovalRepository
from execution_capability.domain.models import ApprovalStatus


def test_request_approval():
    mock_repo = MagicMock(spec=ApprovalRepository)
    mock_repo.save.side_effect = lambda x: x

    service = ApprovalService(mock_repo)

    req = service.request_approval("step_123", "cap_456", "user_789")

    assert req.execution_step_id == "step_123"
    assert req.status == ApprovalStatus.PENDING
