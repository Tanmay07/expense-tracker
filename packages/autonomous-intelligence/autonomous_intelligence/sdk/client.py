from typing import Dict, Any, List, Optional
import httpx


class AutonomousAgentSDK:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def registerAgent(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post("/agents", json=payload)
        response.raise_for_status()
        return response.json()

    async def createMission(
        self,
        agent_id: str,
        name: str,
        hitl_classification: str = "FULLY_AUTOMATED",
        goal_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "agent_id": agent_id,
            "name": name,
            "hitl_classification": hitl_classification,
        }
        if goal_id:
            payload["goal_id"] = goal_id
        response = await self.client.post("/missions", json=payload)
        response.raise_for_status()
        return response.json()

    async def plan(
        self, agent_id: str, horizon: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = await self.client.post(
            "/plans",
            json={"agent_id": agent_id, "horizon": horizon, "context": context},
        )
        response.raise_for_status()
        return response.json()

    async def delegateTask(
        self, source_agent_id: str, target_agent_id: str, task_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = await self.client.post(
            "/collaboration/delegate",
            json={
                "source_agent_id": source_agent_id,
                "target_agent_id": target_agent_id,
                "task_details": task_details,
            },
        )
        response.raise_for_status()
        return response.json()

    async def requestApproval(
        self, agent_id: str, action_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = await self.client.post(
            f"/agents/{agent_id}/approvals", json=action_details
        )
        response.raise_for_status()
        return response.json()

    async def executeWorkflow(
        self, agent_id: str, mission_id: str, steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        response = await self.client.post(
            "/orchestrator/execute",
            json={"agent_id": agent_id, "mission_id": mission_id, "steps": steps},
        )
        response.raise_for_status()
        return response.json()

    async def evaluateAgent(
        self, agent_id: str, metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = await self.client.post(
            f"/agents/{agent_id}/evaluations", json=metrics
        )
        response.raise_for_status()
        return response.json()

    async def getMissionStatus(self, mission_id: str) -> Dict[str, Any]:
        response = await self.client.get(f"/missions/{mission_id}")
        response.raise_for_status()
        return response.json()
