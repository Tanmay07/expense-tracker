from unittest.mock import MagicMock
from execution_capability.application.services import ExecutionCapabilityService, RoutingService
from execution_capability.domain.models import ExecutionCapability, AutomationLevel, RiskLevel
from execution_capability.infrastructure.repositories import CapabilityRepository

def test_capability_registration():
    mock_repo = MagicMock(spec=CapabilityRepository)
    mock_repo.save.side_effect = lambda x: x
    
    service = ExecutionCapabilityService(mock_repo)
    
    cap = ExecutionCapability(
        name="Broker API",
        description="Connects to external broker",
        automation_level=AutomationLevel.FULLY_AUTOMATED,
        risk_level=RiskLevel.MEDIUM
    )
    
    saved = service.register_capability(cap)
    
    assert saved.name == "Broker API"
    assert saved.automation_level == AutomationLevel.FULLY_AUTOMATED

def test_routing_approval_required():
    mock_repo = MagicMock(spec=CapabilityRepository)
    
    cap = ExecutionCapability(
        name="High Risk Action",
        description="Requires approval",
        automation_level=AutomationLevel.APPROVAL_REQUIRED,
        risk_level=RiskLevel.HIGH,
        metadata={"tags": ["crypto", "transfer"]}
    )
    
    mock_repo.list_all.return_value = [cap]
    
    service = RoutingService(mock_repo)
    
    route = service.determine_route("step_123", ["crypto", "transfer"])
    
    assert route is not None
    assert route.selected_capability_id == cap.id
    # Should not be ready because it requires approval
    assert route.is_ready is False

def test_routing_ready():
    mock_repo = MagicMock(spec=CapabilityRepository)
    
    cap = ExecutionCapability(
        name="Low Risk Notification",
        description="Just sends an email",
        automation_level=AutomationLevel.FULLY_AUTOMATED,
        risk_level=RiskLevel.LOW,
        metadata={"tags": ["notification"]}
    )
    
    mock_repo.list_all.return_value = [cap]
    
    service = RoutingService(mock_repo)
    
    route = service.determine_route("step_123", ["notification"])
    
    assert route is not None
    assert route.selected_capability_id == cap.id
    # Should be ready because it is fully automated and low risk
    assert route.is_ready is True
