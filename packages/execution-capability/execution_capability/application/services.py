from typing import Optional, List

from ..domain.models import (
    ExecutionCapability, 
    AutomationLevel, 
    RiskLevel, 
    ExecutionRoute, 
    ApprovalRequest
)
from ..infrastructure.repositories import CapabilityRepository, ApprovalRepository

class ExecutionCapabilityService:
    def __init__(self, repo: CapabilityRepository):
        self.repo = repo

    def register_capability(self, capability: ExecutionCapability) -> ExecutionCapability:
        return self.repo.save(capability)

    def list_capabilities(self) -> List[ExecutionCapability]:
        return self.repo.list_all()

    def get_capability(self, capability_id: str) -> Optional[ExecutionCapability]:
        return self.repo.get_by_id(capability_id)

class RoutingService:
    def __init__(self, capability_repo: CapabilityRepository):
        self.repo = capability_repo
        
    def determine_route(self, step_id: str, required_tags: List[str]) -> Optional[ExecutionRoute]:
        # Simplistic routing: find first active capability matching tags
        capabilities = self.repo.list_all()
        selected = None
        for cap in capabilities:
            if not cap.is_active:
                continue
            # Match if capability metadata contains all required tags
            cap_tags = cap.metadata.get("tags", [])
            if all(tag in cap_tags for tag in required_tags):
                selected = cap
                break
                
        if not selected:
            return None
            
        route = ExecutionRoute(
            step_id=step_id,
            selected_capability_id=selected.id
        )
        
        # Enforce Automation Level constraints
        if selected.automation_level == AutomationLevel.APPROVAL_REQUIRED or selected.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            route.is_ready = False
        else:
            route.is_ready = True
            
        return route

class ApprovalService:
    def __init__(self, repo: ApprovalRepository):
        self.repo = repo
        
    def request_approval(self, execution_step_id: str, capability_id: str, requested_by: str) -> ApprovalRequest:
        req = ApprovalRequest(
            execution_step_id=execution_step_id,
            capability_id=capability_id,
            requested_by=requested_by
        )
        return self.repo.save(req)
        
    def grant_approval(self, request_id: str, approver_id: str) -> Optional[ApprovalRequest]:
        # Fetching would require a get_by_id in the repo, mocking logic for brevity
        pass
