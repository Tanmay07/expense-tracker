import httpx
from typing import Dict, Any, List, Optional

class AnalyticsIntelligenceSDK:
    """
    Unified SDK for the Enterprise Analytics, Experiment Intelligence & Continuous Improvement Platform.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def registerExperiment(self, name: str, business_objective: str, hypothesis: str, owner_id: str, description: str = None, feature_id: str = None) -> Dict[str, Any]:
        data = {
            "name": name,
            "business_objective": business_objective,
            "hypothesis": hypothesis,
            "owner_id": owner_id,
            "description": description,
            "feature_id": feature_id
        }
        resp = self.client.post("/api/v1/experiments/registry", json=data)
        resp.raise_for_status()
        return resp.json()

    def getExperiment(self, name: str) -> Dict[str, Any]:
        resp = self.client.get(f"/api/v1/experiments/registry/{name}")
        resp.raise_for_status()
        return resp.json()

    def calculateMDE(self, baseline: float, sample_size: int, alpha: float = 0.05, power: float = 0.8) -> float:
        data = {
            "baseline_conversion": baseline,
            "sample_size": sample_size,
            "alpha": alpha,
            "power": power
        }
        resp = self.client.post("/api/v1/experiments/guardrails/mde", json=data)
        resp.raise_for_status()
        return resp.json().get("minimum_detectable_effect")

    def registerKPI(self, kpi_name: str, category: str, formula: str, owner_id: str, target: float = None) -> Dict[str, Any]:
        data = {
            "kpi_name": kpi_name,
            "category": category,
            "formula": formula,
            "owner_id": owner_id,
            "target_value": target
        }
        resp = self.client.post("/api/v1/kpis", json=data)
        resp.raise_for_status()
        return resp.json()

    def generateInsight(self, title: str, description: str, severity: str = "INFO") -> Dict[str, Any]:
        data = {
            "title": title,
            "description": description,
            "severity": severity
        }
        resp = self.client.post("/api/v1/insights", json=data)
        resp.raise_for_status()
        return resp.json()

    def generateWeeklyReport(self) -> Dict[str, Any]:
        resp = self.client.post("/api/v1/reports/weekly")
        resp.raise_for_status()
        return resp.json()
