from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from governance_platform.infrastructure.database import SessionLocal
from governance_platform.infrastructure.repositories import (
    PolicyRepository, TrustRepository, MaturityRepository,
    AIGovernanceRepository, EvidenceRepository, WorkflowRepository
)
from governance_platform.application.services import (
    GovernancePolicyService, TrustService, MaturityService,
    AIGovernanceService, EvidenceLedgerService, GovernanceWorkflowService, AssuranceService
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_policy_repo(db: Session = Depends(get_db)) -> PolicyRepository:
    return PolicyRepository(db)

def get_trust_repo(db: Session = Depends(get_db)) -> TrustRepository:
    return TrustRepository(db)

def get_maturity_repo(db: Session = Depends(get_db)) -> MaturityRepository:
    return MaturityRepository(db)

def get_ai_gov_repo(db: Session = Depends(get_db)) -> AIGovernanceRepository:
    return AIGovernanceRepository(db)

def get_evidence_repo(db: Session = Depends(get_db)) -> EvidenceRepository:
    return EvidenceRepository(db)

def get_workflow_repo(db: Session = Depends(get_db)) -> WorkflowRepository:
    return WorkflowRepository(db)


def get_policy_service(repo: PolicyRepository = Depends(get_policy_repo)) -> GovernancePolicyService:
    return GovernancePolicyService(repo)

def get_trust_service(repo: TrustRepository = Depends(get_trust_repo)) -> TrustService:
    return TrustService(repo)

def get_maturity_service(repo: MaturityRepository = Depends(get_maturity_repo)) -> MaturityService:
    return MaturityService(repo)

def get_ai_gov_service(repo: AIGovernanceRepository = Depends(get_ai_gov_repo)) -> AIGovernanceService:
    return AIGovernanceService(repo)

def get_evidence_service(repo: EvidenceRepository = Depends(get_evidence_repo)) -> EvidenceLedgerService:
    return EvidenceLedgerService(repo)

def get_workflow_service(repo: WorkflowRepository = Depends(get_workflow_repo)) -> GovernanceWorkflowService:
    return GovernanceWorkflowService(repo)

def get_assurance_service(
    trust_svc: TrustService = Depends(get_trust_service),
    ledger_svc: EvidenceLedgerService = Depends(get_evidence_service)
) -> AssuranceService:
    return AssuranceService(trust_svc, ledger_svc)
