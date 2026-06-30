import httpx
from typing import Dict, Any, List, Optional

class SandboxSDK:
    """
    SDK for the Enterprise Strategy Sandbox Platform.
    Allows other modules to request validations, execute runs, and query fitness scores.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)
        
    def initiateRun(self, asset_id: str, profile_id: str) -> Dict[str, Any]:
        resp = self.client.post("/api/v1/sandbox/runs", json={"asset_id": asset_id, "profile_id": profile_id})
        resp.raise_for_status()
        return resp.json()
        
    def getRun(self, run_id: str) -> Dict[str, Any]:
        resp = self.client.get(f"/api/v1/sandbox/runs/{run_id}")
        resp.raise_for_status()
        return resp.json()

    def listRuns(self, asset_id: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if asset_id:
            params["asset_id"] = asset_id
        resp = self.client.get("/api/v1/sandbox/runs", params=params)
        resp.raise_for_status()
        return resp.json()
        
    def createProfile(self, dto: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.post("/api/v1/validation-profiles", json=dto)
        resp.raise_for_status()
        return resp.json()
        
    def listProfiles(self) -> List[Dict[str, Any]]:
        resp = self.client.get("/api/v1/validation-profiles")
        resp.raise_for_status()
        return resp.json()
        
    def calculateFitness(self, run_id: str) -> Dict[str, Any]:
        resp = self.client.post(f"/api/v1/fitness/{run_id}")
        resp.raise_for_status()
        return resp.json()
        
    def validatePrompt(self, run_id: str, prompt_text: str) -> Dict[str, Any]:
        resp = self.client.post(f"/api/v1/prompt-validation/{run_id}", params={"prompt_text": prompt_text})
        resp.raise_for_status()
        return resp.json()
