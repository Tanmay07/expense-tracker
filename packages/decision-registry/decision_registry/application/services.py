from typing import List, Optional

from ..domain.models import Decision, DecisionRelationship, DecisionStatus
from ..infrastructure.repositories import DecisionRepository, DecisionRelationshipRepository

class DecisionRegistryService:
    def __init__(self, repo: DecisionRepository):
        self.repo = repo

    def create_decision(self, decision: Decision) -> Decision:
        return self.repo.save(decision)

    def get_decision(self, decision_id: str) -> Optional[Decision]:
        return self.repo.get_by_id(decision_id)
        
    def archive_decision(self, decision_id: str) -> Optional[Decision]:
        decision = self.repo.get_by_id(decision_id)
        if decision:
            decision.status = DecisionStatus.ARCHIVED
            return self.repo.save(decision)
        return None

class DecisionRelationshipService:
    def __init__(self, repo: DecisionRelationshipRepository):
        self.repo = repo

    def add_relationship(self, relationship: DecisionRelationship) -> DecisionRelationship:
        return self.repo.save(relationship)

    def get_relationships(self, decision_id: str) -> List[DecisionRelationship]:
        return self.repo.get_by_decision(decision_id)
