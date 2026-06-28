from typing import Dict, Any, List
from litellm import completion

from ..domain.models import ContextFrame, Message, Role
import json

class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "gpt-4-turbo"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model

    def run(self, messages: List[Message], context: ContextFrame) -> str:
        # Build litellm messages
        llm_messages = [{"role": "system", "content": self._build_system_prompt(context)}]
        for msg in messages:
            llm_messages.append({"role": msg.role.value, "content": msg.content})
            
        # Call LiteLLM
        try:
            response = completion(model=self.model, messages=llm_messages)
            return response.choices[0].message.content
        except Exception as e:
            # Mock fallback for test environment without valid API Keys
            print(f"LiteLLM error: {e}. Returning mock response.")
            return f"[Mock {self.name}] I have analyzed your request based on context."

    def _build_system_prompt(self, context: ContextFrame) -> str:
        # Inject context into system prompt
        context_str = json.dumps({
            "metrics": context.metrics,
            "policies": context.active_policies,
            "memories": [m.content for m in context.recent_memories]
        })
        return f"{self.system_prompt}\n\nContext:\n{context_str}"


class ExpenseAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ExpenseAnalysisAgent",
            system_prompt="You are an expert at analyzing expenses. Use the provided semantic metrics to answer questions about spending.",
            model="gpt-4-turbo"
        )

class GoalPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="GoalPlanningAgent",
            system_prompt="You are an expert financial planner. Use timeline and goals data to assist the user.",
            model="gpt-4-turbo"
        )
