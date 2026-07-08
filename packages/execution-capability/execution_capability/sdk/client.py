import requests
from typing import Dict, Any, List, Optional


class ExecutionCapabilitySDK:
    def __init__(
        self, base_url: str = "http://localhost:8009/api/v1/execution-capability"
    ):
        self.base_url = base_url

    def register_capability(self, capability_data: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(f"{self.base_url}/capabilities", json=capability_data)
        resp.raise_for_status()
        return resp.json()

    def find_capabilities(self) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.base_url}/capabilities")
        resp.raise_for_status()
        return resp.json()

    def plan_execution_route(
        self, step_id: str, required_tags: List[str]
    ) -> Optional[Dict[str, Any]]:
        resp = requests.post(
            f"{self.base_url}/routing",
            json={"step_id": step_id, "required_tags": required_tags},
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    def request_approval(
        self, execution_step_id: str, capability_id: str, requested_by: str
    ) -> Dict[str, Any]:
        payload = {
            "execution_step_id": execution_step_id,
            "capability_id": capability_id,
            "requested_by": requested_by,
        }
        resp = requests.post(f"{self.base_url}/approvals", json=payload)
        resp.raise_for_status()
        return resp.json()
