import httpx
from typing import Dict, Any

class FeatureExperimentationSDK:
    """
    Unified SDK for the Enterprise Feature Flag, Experimentation & Progressive Delivery Platform.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def registerFeature(self, name: str, version: str, feature_type: str, owner_id: str) -> Dict[str, Any]:
        data = {
            "name": name,
            "version": version,
            "feature_type": feature_type,
            "owner_id": owner_id
        }
        resp = self.client.post("/api/v1/features", json=data)
        resp.raise_for_status()
        return resp.json()

    def evaluateFeature(self, feature_id: str, context: Dict[str, Any]) -> bool:
        """
        Evaluates a feature flag based on contextual metadata. Returns True if enabled.
        """
        data = {
            "feature_id": feature_id,
            "context": context
        }
        resp = self.client.post("/api/v1/feature-flags/evaluate", json=data)
        resp.raise_for_status()
        return resp.json().get("is_enabled", False)

    def isFeatureEnabled(self, feature_id: str, context: Dict[str, Any]) -> bool:
        """
        Alias for evaluateFeature.
        """
        return self.evaluateFeature(feature_id, context)

    def assignExperiment(self, experiment_id: str, context: Dict[str, Any]) -> str:
        """
        Deterministically assigns an entity to an experiment bucket.
        """
        data = {
            "experiment_id": experiment_id,
            "context": context
        }
        resp = self.client.post("/api/v1/experiments/assign", json=data)
        resp.raise_for_status()
        return resp.json().get("variant", "control")

    def rollback(self, feature_id: str, reason: str) -> Dict[str, Any]:
        """
        Emergency rollback.
        """
        data = {"reason": reason}
        resp = self.client.post(f"/api/v1/rollback/{feature_id}", json=data)
        resp.raise_for_status()
        return resp.json()
