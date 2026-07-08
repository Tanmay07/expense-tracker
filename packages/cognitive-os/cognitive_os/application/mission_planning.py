from typing import List, Dict, Any, Optional
from ..domain.planning_models import MissionDefinition, MissionPriority, GoalDefinition
import uuid

class MissionPlanningService:
    """
    Generates autonomous missions. Prioritizes based on financial impact, urgency,
    risk, and dependencies.
    """
    def __init__(self):
        self._missions: Dict[str, MissionDefinition] = {}

    def generate_mission_for_goal(self, goal: GoalDefinition, context: Dict[str, Any]) -> MissionDefinition:
        """
        Dynamically generates a mission to advance a specific goal.
        """
        mission_id = f"msn_{uuid.uuid4().hex[:8]}"
        
        # Mock AI generation logic
        priority = MissionPriority.ELEVATED if goal.priority in ("HIGH", "CRITICAL") else MissionPriority.ROUTINE
        
        mission = MissionDefinition(
            id=mission_id,
            goal_id=goal.id,
            title=f"Advance {goal.title}",
            description=f"Auto-generated mission to support goal: {goal.title}",
            priority=priority,
            risk_level="LOW",
            financial_impact_estimate=goal.target_amount * 0.1 if goal.target_amount else 100.0,
            context=context
        )
        self._missions[mission.id] = mission
        return mission

    def prioritize_missions(self, active_missions: List[MissionDefinition]) -> List[MissionDefinition]:
        """
        Sorts missions based on Financial Impact, Urgency (Priority), and Risk.
        """
        def sort_key(m: MissionDefinition):
            priority_weight = {"URGENT": 3, "ELEVATED": 2, "ROUTINE": 1}.get(m.priority.value, 1)
            risk_weight = {"LOW": 1, "MEDIUM": 0.8, "HIGH": 0.5}.get(m.risk_level, 1) # Prefer lower risk
            
            # Score = Impact * Priority Weight * Risk Modifier
            return m.financial_impact_estimate * priority_weight * risk_weight

        return sorted(active_missions, key=sort_key, reverse=True)

    def get_pending_missions(self) -> List[MissionDefinition]:
        return [m for m in self._missions.values() if m.status == "PENDING"]
    
    def update_mission_status(self, mission_id: str, status: str) -> MissionDefinition:
        mission = self._missions.get(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found.")
        mission.status = status
        return mission
