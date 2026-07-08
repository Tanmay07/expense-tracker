from unittest.mock import MagicMock
from datetime import datetime

from decision_registry.application.services import DecisionRegistryService
from decision_registry.domain.models import (
    Decision,
    DecisionType,
    DecisionCategory,
    DecisionScope,
    DecisionPriority,
    DecisionVersion,
    DecisionMetadata,
    DecisionProvenance,
)
from decision_registry.infrastructure.repositories import DecisionRepository


def test_decision_creation_and_retrieval():
    mock_repo = MagicMock(spec=DecisionRepository)

    d = Decision(
        user_id="user_123",
        type=DecisionType.RECOMMENDATION,
        category=DecisionCategory.INVESTMENT,
        scope=DecisionScope.PORTFOLIO,
        priority=DecisionPriority(level="HIGH", importance_score=0.9),
        version_info=DecisionVersion(
            version=1, semantic_version="1.0.0", created_at=datetime.utcnow()
        ),
        metadata=DecisionMetadata(
            source="AI_COACH",
            owner="SYSTEM",
            summary="Buy AAPL",
            narrative="AAPL is good",
        ),
        provenance=DecisionProvenance(
            metrics_used=["AAPL_PE"], policies_used=["MAX_ALLOCATION"]
        ),
    )

    mock_repo.save.return_value = d
    mock_repo.get_by_id.return_value = d

    service = DecisionRegistryService(mock_repo)

    # Test Create
    saved = service.create_decision(d)
    assert saved.id == d.id
    mock_repo.save.assert_called_once_with(d)

    # Test Retrieve
    retrieved = service.get_decision(d.id)
    assert retrieved.id == d.id
    mock_repo.get_by_id.assert_called_once_with(d.id)


def test_decision_archive():
    mock_repo = MagicMock(spec=DecisionRepository)

    d = Decision(
        user_id="user_123",
        type=DecisionType.RECOMMENDATION,
        category=DecisionCategory.INVESTMENT,
        scope=DecisionScope.PORTFOLIO,
        priority=DecisionPriority(level="HIGH", importance_score=0.9),
        version_info=DecisionVersion(
            version=1, semantic_version="1.0.0", created_at=datetime.utcnow()
        ),
        metadata=DecisionMetadata(
            source="AI_COACH",
            owner="SYSTEM",
            summary="Buy AAPL",
            narrative="AAPL is good",
        ),
        provenance=DecisionProvenance(),
    )

    mock_repo.get_by_id.return_value = d
    mock_repo.save.side_effect = lambda x: x

    service = DecisionRegistryService(mock_repo)

    archived = service.archive_decision(d.id)
    assert archived.status == "ARCHIVED"
    mock_repo.save.assert_called_once()
