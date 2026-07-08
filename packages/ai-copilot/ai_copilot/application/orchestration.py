from typing import Dict, Any
from litellm import completion

from ..domain.models import CopilotMode, ActionPlan


class AgentCoordinatorService:
    def __init__(self):
        # Maps modes to specialized agent system prompts
        self.mode_prompts = {
            CopilotMode.DAILY_COACH: "You are a daily financial coach...",
            CopilotMode.BUDGET_COACH: "You are a specialized budget coach...",
            CopilotMode.INVESTMENT_COACH: "You are an investment coach focusing on long-term wealth...",
            CopilotMode.DEBT_COACH: "You are a debt reduction expert...",
            CopilotMode.GOAL_COACH: "You are a goal planning expert...",
        }

    def coordinate_agents(
        self, mode: CopilotMode, context: Dict[str, Any], query: str
    ) -> str:
        prompt = self.mode_prompts.get(mode, "You are an AI financial copilot.")
        # We mock Litellm for deterministic testing or use fallback
        try:
            response = completion(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Context: {context}\nQuery: {query}"},
                ],
            )
            return response.choices[0].message.content
        except Exception:
            return f"[Mock Agent Response for {mode.value}] Analyzed your query."


class DecisionIntelligenceService:
    def evaluate_action_plan(
        self, conversation_id: str, plan: ActionPlan
    ) -> Dict[str, Any]:
        """
        In a real system, this evaluates the action plan against the Knowledge Graph
        and Rules Engine to ensure compliance and feasibility.
        """
        confidence = 0.95
        if plan.priority == "HIGH":
            confidence = 0.88

        return {
            "is_approved": True,
            "confidence": confidence,
            "simulated_impact": plan.expected_impact,
        }
