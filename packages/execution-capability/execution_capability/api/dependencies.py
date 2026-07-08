from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import CapabilityRepository, ApprovalRepository
from ..application.services import (
    ExecutionCapabilityService,
    RoutingService,
    ApprovalService,
)


def get_capability_repo(db: Session = Depends(get_db)):
    return CapabilityRepository(db)


def get_approval_repo(db: Session = Depends(get_db)):
    return ApprovalRepository(db)


def get_capability_svc(
    repo: CapabilityRepository = Depends(get_capability_repo),
) -> ExecutionCapabilityService:
    return ExecutionCapabilityService(repo)


def get_routing_svc(
    repo: CapabilityRepository = Depends(get_capability_repo),
) -> RoutingService:
    return RoutingService(repo)


def get_approval_svc(
    repo: ApprovalRepository = Depends(get_approval_repo),
) -> ApprovalService:
    return ApprovalService(repo)
