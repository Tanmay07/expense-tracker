import os
import httpx
from typing import Dict, Any, Optional


class PlatformReadinessSDK:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("PRAPC_API_URL", "http://localhost:8020")
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def runArchitectureAudit(self, component_name: str) -> Dict[str, Any]:
        resp = self.client.post(
            "/api/v1/readiness/architecture", json={"component_name": component_name}
        )
        resp.raise_for_status()
        return resp.json()

    def runSecurityAssessment(self, component_name: str) -> Dict[str, Any]:
        resp = self.client.post(
            "/api/v1/readiness/security", json={"component_name": component_name}
        )
        resp.raise_for_status()
        return resp.json()

    def runPerformanceCertification(self, endpoint: str) -> Dict[str, Any]:
        resp = self.client.post(
            "/api/v1/readiness/performance", json={"endpoint": endpoint}
        )
        resp.raise_for_status()
        return resp.json()

    def runChaosExperiment(
        self, scenario_name: str, target_component: str
    ) -> Dict[str, Any]:
        resp = self.client.post(
            "/api/v1/readiness/chaos",
            json={"scenario_name": scenario_name, "target_component": target_component},
        )
        resp.raise_for_status()
        return resp.json()

    def validateDisasterRecovery(self) -> Dict[str, Any]:
        pass

    def validateMigration(self) -> Dict[str, Any]:
        pass

    def calculateReadiness(self, version_tag: str) -> Dict[str, Any]:
        resp = self.client.post(
            "/api/v1/readiness/score", json={"version_tag": version_tag}
        )
        resp.raise_for_status()
        return resp.json()

    def generateCertificationReport(self, version_tag: str) -> Dict[str, Any]:
        resp = self.client.get(f"/api/v1/readiness/score/{version_tag}")
        resp.raise_for_status()
        return resp.json()

    def getRiskRegister(self, version_tag: str) -> Optional[Dict[str, Any]]:
        cert = self.generateCertificationReport(version_tag)
        return cert.get("risk_register")

    def generateRemediationPlan(self, version_tag: str) -> Optional[Dict[str, Any]]:
        cert = self.generateCertificationReport(version_tag)
        return cert.get("remediation_plan")
