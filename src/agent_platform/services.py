import uuid
from typing import Dict, Any, List

class ToolRegistryService:
    def __init__(self):
        self.tools = {
            "query_ledger": {"security": "LOW", "description": "Reads ledger balances"},
            "execute_transfer": {"security": "HIGH", "description": "Moves money between accounts"}
        }
        
    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        return self.tools[tool_name]

class PermissionService:
    def __init__(self):
        self.agent_roles = {
            "budget_agent": ["query_ledger"],
            "wealth_agent": ["query_ledger", "execute_transfer"]
        }
        
    def can_execute(self, agent_role: str, tool_name: str) -> bool:
        allowed_tools = self.agent_roles.get(agent_role, [])
        return tool_name in allowed_tools

class PlannerService:
    """
    Mocks an LLM generating a DAG execution plan.
    """
    def generate_plan(self, intent: str) -> List[str]:
        if "transfer" in intent.lower():
            return ["query_ledger", "execute_transfer"]
        return ["query_ledger"]

class ApprovalService:
    def __init__(self):
        # In memory DB of pending approvals
        self.pending_approvals = {}
        
    def request_approval(self, execution_id: str, tool_name: str):
        self.pending_approvals[execution_id] = tool_name
        
    def approve(self, execution_id: str) -> bool:
        if execution_id in self.pending_approvals:
            del self.pending_approvals[execution_id]
            return True
        return False

class ExecutionService:
    """
    Mocks a Temporal workflow engine executing the tools.
    """
    def __init__(self, tool_registry: ToolRegistryService, permissions: PermissionService, approval: ApprovalService):
        self.tools = tool_registry
        self.permissions = permissions
        self.approval = approval
        
    def execute_plan(self, agent_role: str, plan: List[str]) -> Dict[str, Any]:
        execution_id = str(uuid.uuid4())
        executed_tools = []
        
        for tool_name in plan:
            if not self.permissions.can_execute(agent_role, tool_name):
                return {"status": "failed", "reason": f"Permission denied for {tool_name}"}
                
            tool_meta = self.tools.get_tool(tool_name)
            
            # HITL Checkpoint
            if tool_meta["security"] == "HIGH":
                self.approval.request_approval(execution_id, tool_name)
                return {
                    "status": "paused", 
                    "reason": "Human approval required", 
                    "execution_id": execution_id,
                    "pending_tool": tool_name,
                    "executed_so_far": executed_tools
                }
                
            executed_tools.append(tool_name)
            
        return {"status": "completed", "executed_tools": executed_tools}
