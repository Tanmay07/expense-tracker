import requests
from typing import Dict, Any

class ExecutionPolicySDK:
    def __init__(self, base_url: str = "http://localhost:8010/api/v1/execution-policy"):
        self.base_url = base_url

    def register_policy(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(f"{self.base_url}/policies", json=policy_data)
        resp.raise_for_status()
        return resp.json()

    def evaluate(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a context snapshot against all active policies.
        Returns the EvaluationResult containing outcome and explanation.
        """
        resp = requests.post(f"{self.base_url}/evaluate", json=context_data)
        resp.raise_for_status()
        return resp.json()
