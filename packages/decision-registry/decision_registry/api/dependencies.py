from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import DecisionRepository, DecisionRelationshipRepository
from ..application.services import DecisionRegistryService, DecisionRelationshipService
from ..application.sdk import DecisionSDK

def get_decision_repo(db: Session = Depends(get_db)):
    return DecisionRepository(db)

def get_relationship_repo(db: Session = Depends(get_db)):
    return DecisionRelationshipRepository(db)

def get_sdk(
    decision_repo: DecisionRepository = Depends(get_decision_repo),
    rel_repo: DecisionRelationshipRepository = Depends(get_relationship_repo)
) -> DecisionSDK:
    registry_svc = DecisionRegistryService(decision_repo)
    rel_svc = DecisionRelationshipService(rel_repo)
    return DecisionSDK(registry_svc, rel_svc)
