from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import LifecycleRepository, ExecutionPlanRepository
from ..application.services import DecisionLifecycleService, ExecutionPlannerService


def get_lifecycle_repo(db: Session = Depends(get_db)):
    return LifecycleRepository(db)


def get_plan_repo(db: Session = Depends(get_db)):
    return ExecutionPlanRepository(db)


def get_lifecycle_svc(
    repo: LifecycleRepository = Depends(get_lifecycle_repo),
) -> DecisionLifecycleService:
    return DecisionLifecycleService(repo)


def get_planner_svc(
    repo: ExecutionPlanRepository = Depends(get_plan_repo),
) -> ExecutionPlannerService:
    return ExecutionPlannerService(repo)
