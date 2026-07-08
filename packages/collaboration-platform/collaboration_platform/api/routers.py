from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from collaboration_platform.domain.models import (
    Household, HouseholdMember, MemberRole, Advisor, Delegation, DelegationScope,
    SharedWorkspace
)
from collaboration_platform.application.services import (
    HouseholdService, DelegationService, AdvisorService, WorkspaceSharingService
)
from collaboration_platform.infrastructure.database import get_db_session
from collaboration_platform.infrastructure.repositories import (
    HouseholdRepository, DelegationRepository, AdvisorRepository, WorkspaceRepository
)

router = APIRouter(prefix="/api/v1/collaboration", tags=["Collaboration"])

def get_household_service(session=Depends(get_db_session)) -> HouseholdService:
    return HouseholdService(HouseholdRepository(session))

def get_delegation_service(session=Depends(get_db_session)) -> DelegationService:
    return DelegationService(DelegationRepository(session))

def get_advisor_service(session=Depends(get_db_session)) -> AdvisorService:
    return AdvisorService(AdvisorRepository(session))

def get_workspace_service(session=Depends(get_db_session)) -> WorkspaceSharingService:
    return WorkspaceSharingService(WorkspaceRepository(session))

# --- DTOs ---

class CreateHouseholdRequest(BaseModel):
    name: str
    owner_id: str

class AddMemberRequest(BaseModel):
    user_id: str
    role: MemberRole

class DelegateRequest(BaseModel):
    delegator_user_id: str
    delegatee_user_id: str
    scope: DelegationScope
    household_id: Optional[str] = None
    expires_at: Optional[datetime] = None

class RegisterAdvisorRequest(BaseModel):
    user_id: str
    specialty: str
    firm_name: Optional[str] = None

class CreateWorkspaceRequest(BaseModel):
    name: str
    owner_id: str
    household_id: Optional[str] = None

# --- Routes ---

@router.post("/households", response_model=Household)
async def create_household(req: CreateHouseholdRequest, svc: HouseholdService = Depends(get_household_service)):
    return await svc.create_household(req.name, req.owner_id)

@router.post("/households/{household_id}/members", response_model=HouseholdMember)
async def add_member(household_id: str, req: AddMemberRequest, svc: HouseholdService = Depends(get_household_service)):
    return await svc.add_member(household_id, req.user_id, req.role)

@router.post("/advisors", response_model=Advisor)
async def register_advisor(req: RegisterAdvisorRequest, svc: AdvisorService = Depends(get_advisor_service)):
    return await svc.register_advisor(req.user_id, req.specialty, req.firm_name)

@router.post("/delegations", response_model=Delegation)
async def create_delegation(req: DelegateRequest, svc: DelegationService = Depends(get_delegation_service)):
    return await svc.delegate_authority(req.delegator_user_id, req.delegatee_user_id, req.scope, req.household_id, req.expires_at)

@router.post("/shared-spaces", response_model=SharedWorkspace)
async def create_shared_space(req: CreateWorkspaceRequest, svc: WorkspaceSharingService = Depends(get_workspace_service)):
    return await svc.create_shared_workspace(req.name, req.owner_id, req.household_id)
