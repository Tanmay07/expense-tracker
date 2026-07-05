from typing import List, Dict, Any, Optional
from mission_control.domain.models.ai import ToolConfig, ToolInvocation, ApprovalStatus, AICapability

class CapabilityRegistryService:
    def __init__(self):
        self._capabilities: Dict[str, AICapability] = {}
        self._register_default_capabilities()
        
    def _register_default_capabilities(self):
        self.register_capability(AICapability(
            id="cap_chat_01",
            name="Chat",
            description="General conversational AI capability.",
            version="1.0.0",
            category="Interaction",
            supported_input_types=["text"],
            supported_output_types=["text", "markdown"],
            streaming_support=True,
            multimodal_support=False,
            requires_approval=False,
            expected_latency="low",
            offline_availability=False
        ))
        
        self.register_capability(AICapability(
            id="cap_financial_analysis_01",
            name="Financial Analysis",
            description="Analyze spending patterns and cash flow.",
            version="1.2.0",
            category="Analysis",
            supported_input_types=["text", "structured_data"],
            supported_output_types=["text", "chart", "table"],
            streaming_support=True,
            multimodal_support=False,
            requires_approval=False,
            expected_latency="medium",
            offline_availability=False
        ))
        
        self.register_capability(AICapability(
            id="cap_receipt_ocr_01",
            name="Receipt OCR",
            description="Extract structured data from receipt images.",
            version="2.0.0",
            category="Extraction",
            supported_input_types=["image/jpeg", "image/png", "application/pdf"],
            supported_output_types=["structured_data"],
            streaming_support=False,
            multimodal_support=True,
            requires_approval=False,
            expected_latency="high",
            offline_availability=False
        ))

    def register_capability(self, capability: AICapability) -> None:
        self._capabilities[capability.id] = capability
        
    def get_capability(self, capability_id: str) -> Optional[AICapability]:
        return self._capabilities.get(capability_id)
        
    def list_capabilities(self) -> List[AICapability]:
        return list(self._capabilities.values())

class ToolRegistryService:
    def __init__(self):
        self._tools: Dict[str, ToolConfig] = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        self.register_tool(ToolConfig(
            name="SearchTransactions",
            description="Search and filter financial transactions.",
            schema_definition={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            },
            requires_approval=False
        ))
        
        self.register_tool(ToolConfig(
            name="CreateBudget",
            description="Create a new budget for a specific category.",
            schema_definition={
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "amount": {"type": "number"}
                },
                "required": ["category", "amount"]
            },
            requires_approval=True,
            permissions=["budget:write"]
        ))
        
    def register_tool(self, tool: ToolConfig) -> None:
        self._tools[tool.name] = tool
        
    def get_tool(self, name: str) -> Optional[ToolConfig]:
        return self._tools.get(name)
        
    def list_tools(self) -> List[ToolConfig]:
        return list(self._tools.values())

class ApprovalUIService:
    def __init__(self):
        self._pending_approvals: Dict[str, ToolInvocation] = {}
        
    def request_approval(self, invocation: ToolInvocation) -> ToolInvocation:
        invocation.status = "PENDING"
        invocation.approval_status = ApprovalStatus.PENDING
        self._pending_approvals[invocation.id] = invocation
        return invocation
        
    def process_approval(self, invocation_id: str, status: ApprovalStatus, user_id: str) -> Optional[ToolInvocation]:
        invocation = self._pending_approvals.get(invocation_id)
        if not invocation:
            return None
            
        invocation.approval_status = status
        if status == ApprovalStatus.APPROVED:
            invocation.status = "EXECUTING"
            # Actual execution would happen here or be dispatched
        else:
            invocation.status = "REJECTED"
            invocation.error = "User rejected the action."
            
        del self._pending_approvals[invocation_id]
        return invocation
