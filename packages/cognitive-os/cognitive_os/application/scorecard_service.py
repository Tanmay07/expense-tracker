from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class ScorecardMetrics(BaseModel):
    user_id: str
    goal_completion_rate: float
    financial_improvement_usd: float
    recommendation_acceptance_rate: float
    mission_success_rate: float
    user_trust_score: float
    avg_reasoning_latency_ms: float
    ai_inference_cost_usd: float
    timestamp: str

class CognitiveScorecardService:
    """
    Tracks the overall effectiveness, cost, and trust metrics of the CFOS.
    """
    
    def __init__(self):
        self._scorecards: Dict[str, List[ScorecardMetrics]] = {}

    def record_metrics(self, user_id: str, metrics_update: Dict[str, Any]) -> ScorecardMetrics:
        """
        Updates the scorecard for a user based on recent activity.
        """
        if user_id not in self._scorecards:
            self._scorecards[user_id] = []
            
        # Merge with previous or initialize
        current = ScorecardMetrics(
            user_id=user_id,
            goal_completion_rate=metrics_update.get("goal_completion_rate", 0.0),
            financial_improvement_usd=metrics_update.get("financial_improvement_usd", 0.0),
            recommendation_acceptance_rate=metrics_update.get("recommendation_acceptance_rate", 0.0),
            mission_success_rate=metrics_update.get("mission_success_rate", 0.0),
            user_trust_score=metrics_update.get("user_trust_score", 0.5), # 0.0 to 1.0
            avg_reasoning_latency_ms=metrics_update.get("avg_reasoning_latency_ms", 0.0),
            ai_inference_cost_usd=metrics_update.get("ai_inference_cost_usd", 0.0),
            timestamp=datetime.utcnow().isoformat()
        )
        
        self._scorecards[user_id].append(current)
        return current

    def get_latest_scorecard(self, user_id: str) -> Optional[ScorecardMetrics]:  # noqa: F821
        history = self._scorecards.get(user_id, [])
        if not history:
            return None
        return history[-1]
