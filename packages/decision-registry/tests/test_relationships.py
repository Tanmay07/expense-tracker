from unittest.mock import MagicMock
from decision_registry.application.services import DecisionRelationshipService
from decision_registry.domain.models import DecisionRelationship, DecisionRelationshipType
from decision_registry.infrastructure.repositories import DecisionRelationshipRepository

def test_add_and_get_relationships():
    mock_repo = MagicMock(spec=DecisionRelationshipRepository)
    
    rel = DecisionRelationship(
        source_decision_id="dec_1",
        target_id="goal_1",
        target_type="GOAL",
        relationship_type=DecisionRelationshipType.SUPPORTS_GOAL,
        metadata={}
    )
    
    mock_repo.save.return_value = rel
    mock_repo.get_by_decision.return_value = [rel]
    
    service = DecisionRelationshipService(mock_repo)
    
    # Add
    saved = service.add_relationship(rel)
    assert saved.id == rel.id
    mock_repo.save.assert_called_once_with(rel)
    
    # Get
    rels = service.get_relationships("dec_1")
    assert len(rels) == 1
    assert rels[0].target_id == "goal_1"
    mock_repo.get_by_decision.assert_called_once_with("dec_1")
