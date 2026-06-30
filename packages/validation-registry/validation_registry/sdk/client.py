import httpx
from typing import Dict, Any, List, Optional
import json

class ValidationArtifactSDK:
    """
    SDK for the Enterprise Validation Artifact Registry.
    Provides methods to register, search, link lineage, and package evidence.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def registerArtifact(self, metadata: Dict[str, Any], payload_bytes: bytes) -> Dict[str, Any]:
        files = {
            "payload_file": ("artifact.bin", payload_bytes, "application/octet-stream"),
        }
        data = {
            "metadata": json.dumps(metadata)
        }
        resp = self.client.post("/api/v1/artifacts", files=files, data=data)
        resp.raise_for_status()
        return resp.json()

    def searchArtifacts(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if category:
            params["category"] = category
        resp = self.client.get("/api/v1/artifacts", params=params)
        resp.raise_for_status()
        return resp.json()

    def getArtifact(self, artifact_id: str) -> Dict[str, Any]:
        resp = self.client.get(f"/api/v1/artifacts/{artifact_id}")
        resp.raise_for_status()
        return resp.json()

    def getLineage(self, artifact_id: str) -> List[Dict[str, Any]]:
        resp = self.client.get(f"/api/v1/artifacts/{artifact_id}/lineage")
        resp.raise_for_status()
        return resp.json()

    def checkReuse(self, target_id: str, input_hash: str) -> Dict[str, Any]:
        params = {"target_id": target_id, "input_hash": input_hash}
        resp = self.client.post("/api/v1/reuse/evaluate", params=params)
        resp.raise_for_status()
        return resp.json()

    def generateEvidencePackage(self, name: str, artifact_ids: List[str]) -> Dict[str, Any]:
        payload = {"name": name, "artifact_ids": artifact_ids}
        resp = self.client.post("/api/v1/evidence", json=payload)
        resp.raise_for_status()
        return resp.json()
