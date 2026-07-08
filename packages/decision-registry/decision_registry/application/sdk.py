from typing import Optional, List
from .services import DecisionRegistryService, DecisionRelationshipService
from ..domain.models import Decision, DecisionRelationship


class DecisionSDK:
    """
    The unified interface for creating and managing Decisions across the
    Personal Finance Operating System.
    """

    def __init__(
        self,
        registry_svc: DecisionRegistryService,
        rel_svc: DecisionRelationshipService,
    ):
        self.registry_svc = registry_svc
        self.rel_svc = rel_svc

    def create_decision(self, decision: Decision) -> Decision:
        return self.registry_svc.create_decision(decision)

    def get_decision(self, decision_id: str) -> Optional[Decision]:
        return self.registry_svc.get_decision(decision_id)

    def archive_decision(self, decision_id: str) -> Optional[Decision]:
        return self.registry_svc.archive_decision(decision_id)

    def add_relationship(
        self, relationship: DecisionRelationship
    ) -> DecisionRelationship:
        return self.rel_svc.add_relationship(relationship)

    def get_relationships(self, decision_id: str) -> List[DecisionRelationship]:
        return self.rel_svc.get_relationships(decision_id)
