from fastapi import Depends
from sqlalchemy.orm import Session

from ..infrastructure.database import get_db
from ..infrastructure.repositories import (
    RiskProfileRepository, PolicyRepository, SuitabilityRepository,
    ConstraintRepository, DecisionRepository
)
from ..application.services import (
    SuitabilityService, ComplianceService, PolicyService, ExplainabilityService
)

def get_risk_repo(db: Session = Depends(get_db)) -> RiskProfileRepository:
    return RiskProfileRepository(db)

def get_policy_repo(db: Session = Depends(get_db)) -> PolicyRepository:
    return PolicyRepository(db)

def get_suitability_repo(db: Session = Depends(get_db)) -> SuitabilityRepository:
    return SuitabilityRepository(db)
    
def get_constraint_repo(db: Session = Depends(get_db)) -> ConstraintRepository:
    return ConstraintRepository(db)

def get_decision_repo(db: Session = Depends(get_db)) -> DecisionRepository:
    return DecisionRepository(db)

def get_suitability_service(
    suitability_repo: SuitabilityRepository = Depends(get_suitability_repo),
    risk_repo: RiskProfileRepository = Depends(get_risk_repo)
) -> SuitabilityService:
    return SuitabilityService(suitability_repo, risk_repo)

def get_compliance_service(
    policy_repo: PolicyRepository = Depends(get_policy_repo),
    decision_repo: DecisionRepository = Depends(get_decision_repo)
) -> ComplianceService:
    return ComplianceService(policy_repo, decision_repo)

def get_policy_service(
    policy_repo: PolicyRepository = Depends(get_policy_repo)
) -> PolicyService:
    return PolicyService(policy_repo)

def get_explainability_service(
    decision_repo: DecisionRepository = Depends(get_decision_repo)
) -> ExplainabilityService:
    return ExplainabilityService(decision_repo)
