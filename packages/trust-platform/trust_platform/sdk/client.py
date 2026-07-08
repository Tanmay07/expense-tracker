import httpx
from typing import Dict, Any, Optional


class TrustClient:
    def __init__(self, base_url: str = "http://trust-platform:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def log_audit_event(
        self,
        event_type: str,
        actor_id: str,
        action: str,
        target_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        response = await self.client.post(
            "/api/v1/trust/audit",
            json={
                "event_type": event_type,
                "actor_id": actor_id,
                "action": action,
                "target_id": target_id,
                "metadata": metadata,
            },
        )
        return response.status_code == 200

    async def log_ai_execution(
        self,
        capability_used: str,
        reasoning_summary: str,
        confidence: float,
        safety_checks: Dict[str, bool],
        bias_evaluation: Dict[str, Any],
    ) -> bool:
        response = await self.client.post(
            "/api/v1/trust/ai",
            json={
                "capability_used": capability_used,
                "reasoning_summary": reasoning_summary,
                "confidence": confidence,
                "safety_checks": safety_checks,
                "bias_evaluation": bias_evaluation,
            },
        )
        return response.status_code == 200
