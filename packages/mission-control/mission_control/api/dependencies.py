from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import (
    MissionRepository,
    OpportunityRepository,
    RiskRepository,
)
from ..application.services import (
    MissionControlService,
    PriorityService,
    MissionGeneratorService,
    OpportunityService,
    RiskService,
)


def get_mission_repo(db: Session = Depends(get_db)):
    return MissionRepository(db)


def get_opportunity_repo(db: Session = Depends(get_db)):
    return OpportunityRepository(db)


def get_risk_repo(db: Session = Depends(get_db)):
    return RiskRepository(db)


def get_mission_control_service(
    repo: MissionRepository = Depends(get_mission_repo),
) -> MissionControlService:
    priority_svc = PriorityService()
    gen_svc = MissionGeneratorService()
    return MissionControlService(repo, priority_svc, gen_svc)


def get_opportunity_service(
    repo: OpportunityRepository = Depends(get_opportunity_repo),
) -> OpportunityService:
    return OpportunityService(repo)


def get_risk_service(repo: RiskRepository = Depends(get_risk_repo)) -> RiskService:
    return RiskService(repo)
