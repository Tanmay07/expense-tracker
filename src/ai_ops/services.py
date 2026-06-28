import random
from typing import Dict, Any, List

class MLflowAdapter:
    """
    Mock wrapper around an isolated MLflow container.
    """
    def register_model(self, model_name: str, metrics: Dict[str, float]) -> str:
        # In production this makes REST calls to MLflow tracking server
        version = f"v{random.randint(1, 100)}"
        return f"Registered {model_name} version {version} with F1: {metrics.get('f1_score', 0.0)}"

class PromptRegistryService:
    """
    Manages custom PostgreSQL schema for Prompt Templates.
    Handles A/B testing logic for prompts.
    """
    def __init__(self):
        self.prompts = {
            "financial_coach_v1": "You are a strict financial advisor...",
            "financial_coach_v2": "You are an empathetic financial coach..."
        }
        
    def get_active_prompt(self, template_name: str, user_id: str) -> str:
        # Simple A/B test split based on user_id hash parity
        if hash(user_id) % 2 == 0:
            return self.prompts.get(f"{template_name}_v1", "Default Prompt")
        else:
            return self.prompts.get(f"{template_name}_v2", "Default Prompt")

class MonitoringService:
    """
    Detects Data Drift by performing mock Kolmogorov-Smirnov statistical tests 
    between current production features and training baselines.
    """
    def check_drift(self, feature_name: str, current_value: float, baseline_mean: float) -> Dict[str, Any]:
        # Mock logic: if current value deviates > 30% from baseline, flag drift
        deviation = abs(current_value - baseline_mean) / baseline_mean
        is_drifting = deviation > 0.30
        
        return {
            "feature": feature_name,
            "drift_detected": is_drifting,
            "deviation_percentage": round(deviation * 100, 2),
            "action": "Trigger Retraining" if is_drifting else "None"
        }
