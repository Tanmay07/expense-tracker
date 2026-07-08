from typing import List, Dict
from ..domain.planning_models import GoalDefinition, TimeHorizon

class GoalEngine:
    """
    Evaluates and adapts financial roadmaps across time horizons (Daily to Generational).
    """
    def __init__(self):
        # In a real system, this would interact with the Knowledge Graph / DB.
        self._goals: Dict[str, GoalDefinition] = {}

    def create_goal(self, goal: GoalDefinition) -> GoalDefinition:
        self._goals[goal.id] = goal
        return goal

    def get_goals_by_horizon(self, horizon: TimeHorizon) -> List[GoalDefinition]:
        return [g for g in self._goals.values() if g.horizon == horizon]

    def evaluate_progress(self, goal_id: str, new_amount: float) -> GoalDefinition:
        goal = self._goals.get(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found.")
        
        goal.current_amount = new_amount
        if goal.target_amount and goal.current_amount >= goal.target_amount:
            goal.status = "COMPLETED"
            
        self._goals[goal_id] = goal
        return goal

    def generate_adaptive_roadmap(self, user_id: str) -> Dict[str, Any]:  # noqa: F821
        """
        Analyzes all goals and generates a prioritized timeline.
        """
        active_goals = [g for g in self._goals.values() if g.status == "ACTIVE"]
        
        # Sort by horizon urgency and priority
        # Mock logic
        return {
            "user_id": user_id,
            "immediate_focus": [g.id for g in active_goals if g.horizon in (TimeHorizon.DAILY, TimeHorizon.WEEKLY)],
            "long_term_focus": [g.id for g in active_goals if g.horizon in (TimeHorizon.RETIREMENT, TimeHorizon.GENERATIONAL_WEALTH)]
        }
