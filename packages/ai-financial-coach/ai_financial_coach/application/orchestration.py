from typing import List, Dict, Any, Tuple
from ..domain.models import ContextFrame, Message, Role, Conversation
from .agents import BaseAgent, ExpenseAnalysisAgent, GoalPlanningAgent

class ContextService:
    def build_context(self, user_id: str, query: str) -> ContextFrame:
        # This service orchestrates GraphRAG and semantic retrievals.
        # In a real implementation, it queries the Platform SDKs.
        return ContextFrame(
            metrics={"monthly_spend": 5000, "savings_rate": 0.2},
            active_policies=[{"name": "Max Crypto", "limit": 0.05}],
            recent_memories=[]
        )

class AgentCoordinatorService:
    def __init__(self):
        self.agents = {
            "expense": ExpenseAnalysisAgent(),
            "goal": GoalPlanningAgent()
        }
        
    def route_query(self, query: str) -> BaseAgent:
        # Simple intent routing, would use LLM or classifier in production
        if "spend" in query.lower() or "expense" in query.lower():
            return self.agents["expense"]
        return self.agents["goal"]

class GraphRAGService:
    def retrieve(self, query: str) -> Dict[str, Any]:
        return {"entities": ["Food", "Transport"], "relationships": []}

class ExplainabilityService:
    def generate_explanation(self, response: str, context: ContextFrame) -> Dict[str, Any]:
        return {
            "metrics_used": list(context.metrics.keys()),
            "policies_checked": [p["name"] for p in context.active_policies],
            "confidence": 0.92
        }
