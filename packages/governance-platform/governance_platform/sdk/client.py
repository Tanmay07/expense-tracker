import httpx
from typing import Dict, Any

class GovernanceSDK:
    """
    SDK for the Enterprise Governance, Trust & Assurance Platform.
    Provides methods to evaluate governance, calculate trust, and verify evidence.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def evaluateGovernance(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.post("/api/v1/policies", json=policy)
        resp.raise_for_status()
        return resp.json()

    def calculateTrust(self, asset_id: str) -> Dict[str, Any]:
        resp = self.client.post(f"/api/v1/trust/{asset_id}")
        resp.raise_for_status()
        return resp.json()

    def verifyEvidence(self, asset_id: str, evidence_type: str, raw_payload: str, signer_id: str) -> Dict[str, Any]:
        payload = {
            "evidence_type": evidence_type,
            "raw_payload": raw_payload,
            "signer_id": signer_id
        }
        resp = self.client.post(f"/api/v1/evidence/{asset_id}", json=payload)
        resp.raise_for_status()
        return resp.json()

    def approve(self, asset_id: str, comments: str = None) -> Dict[str, Any]:
        payload = {
            "workflow_type": "PROMOTION",
            "new_state": "APPROVED",
            "comments": comments
        }
        resp = self.client.post(f"/api/v1/workflows/{asset_id}", json=payload)
        resp.raise_for_status()
        return resp.json()

    def runAssurance(self, asset_id: str) -> Dict[str, Any]:
        resp = self.client.post(f"/api/v1/assurance/{asset_id}")
        resp.raise_for_status()
        return resp.json()
