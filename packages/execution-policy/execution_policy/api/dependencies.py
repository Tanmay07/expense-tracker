from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import PolicyRepository, EvaluationRepository
from ..application.services import PolicyRegistryService, PolicyEvaluationService


def get_policy_repo(db: Session = Depends(get_db)):
    return PolicyRepository(db)


def get_eval_repo(db: Session = Depends(get_db)):
    return EvaluationRepository(db)


def get_registry_svc(
    repo: PolicyRepository = Depends(get_policy_repo),
) -> PolicyRegistryService:
    return PolicyRegistryService(repo)


def get_eval_svc(
    policy_repo: PolicyRepository = Depends(get_policy_repo),
    eval_repo: EvaluationRepository = Depends(get_eval_repo),
) -> PolicyEvaluationService:
    return PolicyEvaluationService(policy_repo, eval_repo)
