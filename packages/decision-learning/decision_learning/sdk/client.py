import httpx
from typing import Dict, Any, Optional

class DecisionLearningClient:
    def __init__(self, base_url: str = "http://decision-learning:8000"):
        self.base_url = base_url.rstrip("/")

    def _post(self, endpoint: str, json: dict) -> dict:
        response = httpx.post(f"{self.base_url}{endpoint}", json=json)
        response.raise_for_status()
        return response.json()

    def _get(self, endpoint: str) -> dict:
        response = httpx.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()

    def record_decision_memory(self, decision_id: str, user_id: str, action_type: str, evidence: dict, context: dict, policy: dict) -> dict:
        payload = {
            "decision_id": decision_id,
            "user_id": user_id,
            "action_type": action_type,
            "evidence_json": evidence,
            "context_snapshot_json": context,
            "policy_snapshot_json": policy
        }
        return self._post("/api/v1/learning/decision-memory", json=payload)

    def check_policy_cache(self, decision_id: str, policy_version: int) -> Optional[dict]:
        try:
            return self._get(f"/api/v1/learning/policy-cache/{decision_id}?policy_version={policy_version}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    def get_financial_dna(self, user_id: str) -> Optional[dict]:
        try:
            return self._get(f"/api/v1/learning/financial-dna/{user_id}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    def get_success_prediction(self, decision_id: str) -> Optional[dict]:
        try:
            return self._get(f"/api/v1/learning/predictions/{decision_id}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
