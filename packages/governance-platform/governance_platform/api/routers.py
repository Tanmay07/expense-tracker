from fastapi import APIRouter, Depends
from pydantic import BaseModel

from governance_platform.domain.models import (
    GovernancePolicy,
    GovernancePolicyCreate,
    TrustScore,
    MaturityRecord,
    AIGovernanceRecord,
    AIGovernanceRecordCreate,
    EvidenceLedgerEntry,
    WorkflowState,
)
from governance_platform.application.services import (
    GovernancePolicyService,
    TrustService,
    MaturityService,
    AIGovernanceService,
    EvidenceLedgerService,
    GovernanceWorkflowService,
    AssuranceService,
)
from governance_platform.api.dependencies import (
    get_policy_service,
    get_trust_service,
    get_maturity_service,
    get_ai_gov_service,
    get_evidence_service,
    get_workflow_service,
    get_assurance_service,
)

router = APIRouter()


@router.post("/policies", response_model=GovernancePolicy)
def create_policy(
    dto: GovernancePolicyCreate,
    svc: GovernancePolicyService = Depends(get_policy_service),
):
    return svc.declare_policy(dto)


@router.post("/trust/{asset_id}", response_model=TrustScore)
def calculate_trust(asset_id: str, svc: TrustService = Depends(get_trust_service)):
    return svc.calculate_trust(asset_id)


class MaturityPromoteReq(BaseModel):
    new_level: str
    promoted_by: str
    reason: str


@router.post("/maturity/{asset_id}", response_model=MaturityRecord)
def promote_asset(
    asset_id: str,
    req: MaturityPromoteReq,
    svc: MaturityService = Depends(get_maturity_service),
):
    return svc.promote_asset(asset_id, req.new_level, req.promoted_by, req.reason)


@router.post("/ai-governance", response_model=AIGovernanceRecord)
def record_ai_metrics(
    dto: AIGovernanceRecordCreate,
    svc: AIGovernanceService = Depends(get_ai_gov_service),
):
    return svc.record_metrics(dto)


class EvidenceRecordReq(BaseModel):
    evidence_type: str
    raw_payload: str
    signer_id: str


@router.post("/evidence/{asset_id}", response_model=EvidenceLedgerEntry)
def record_evidence(
    asset_id: str,
    req: EvidenceRecordReq,
    svc: EvidenceLedgerService = Depends(get_evidence_service),
):
    return svc.record_evidence(
        asset_id, req.evidence_type, req.raw_payload, req.signer_id
    )


class WorkflowTransitionReq(BaseModel):
    workflow_type: str
    new_state: str
    comments: str = None


@router.post("/workflows/{asset_id}", response_model=WorkflowState)
def transition_workflow(
    asset_id: str,
    req: WorkflowTransitionReq,
    svc: GovernanceWorkflowService = Depends(get_workflow_service),
):
    return svc.transition_state(
        asset_id, req.workflow_type, req.new_state, req.comments
    )


@router.post("/assurance/{asset_id}")
def run_continuous_assurance(
    asset_id: str, svc: AssuranceService = Depends(get_assurance_service)
):
    result = svc.verify_asset(asset_id)
    return {"asset_id": asset_id, "is_trusted": result}
