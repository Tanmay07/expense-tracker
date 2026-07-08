from typing import Dict, Any
from datetime import datetime
from ..domain.cognitive_models import ReflectionResult
from ..infrastructure.db import DurablePostgresRepository

class ReflectionEngine:
    """
    Evaluates the outcome of completed missions to feed the Learning Platform.
    Compares predicted financial impact vs actual impact.
    """
    def __init__(self, db: DurablePostgresRepository):
        self.db = db
    
    def evaluate_mission_outcome(self, mission_id: str, execution_data: Dict[str, Any]) -> ReflectionResult:
        """
        Analyzes the result of a mission after it has been executed.
        """
        predicted = execution_data.get("predicted_impact", 0.0)
        actual = execution_data.get("actual_impact", 0.0)
        
        # Calculate success score (1.0 is perfect prediction/execution)
        # Prevent division by zero
        if predicted == 0 and actual == 0:
            success_score = 1.0
        elif predicted == 0:
            success_score = 0.5
        else:
            variance = abs(predicted - actual) / abs(predicted)
            success_score = max(0.0, 1.0 - variance)
        
        lessons = []
        improvements = []
        
        if success_score < 0.5:
            lessons.append(f"Mission failed to achieve predicted impact. Expected: {predicted}, Actual: {actual}")
            improvements.append("Adjust risk tolerance models or verify external API latency.")
        else:
            lessons.append("Mission executed successfully within expected parameters.")
            
        return ReflectionResult(
            mission_id=mission_id,
            success_score=success_score,
            predicted_impact=predicted,
            actual_impact=actual,
            lessons_learned=lessons,
            improvement_recommendations=improvements,
            timestamp=datetime.utcnow().isoformat()
        )
