import httpx
from typing import Dict, Any, List, Optional

class OperationalTelemetrySDK:
    """
    Unified SDK for the Enterprise Observability & Telemetry Platform.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def recordEvent(self, category: str, source: str, payload: Dict[str, Any], trace_id: str = None) -> Dict[str, Any]:
        data = {
            "category": category,
            "source": source,
            "payload": payload,
            "trace_id": trace_id
        }
        resp = self.client.post("/api/v1/telemetry", json=data)
        resp.raise_for_status()
        return resp.json()

    def recordMetric(self, metric_name: str, metric_type: str, value: float, tags: Dict[str, str] = None) -> Dict[str, Any]:
        data = {
            "metric_name": metric_name,
            "metric_type": metric_type,
            "value": value,
            "tags": tags
        }
        resp = self.client.post("/api/v1/metrics", json=data)
        resp.raise_for_status()
        return resp.json()

    def recordAIEvent(self, source: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        data = {
            "source": source,
            "metrics": metrics
        }
        resp = self.client.post("/api/v1/ai-observability", json=data)
        resp.raise_for_status()
        return resp.json()

    def recordFinancialEvent(self, source: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        data = {
            "source": source,
            "event_data": event_data
        }
        resp = self.client.post("/api/v1/financial-observability", json=data)
        resp.raise_for_status()
        return resp.json()

    def reportIncident(self, title: str, severity: str, details: Dict[str, Any]) -> Dict[str, Any]:
        data = {
            "title": title,
            "severity": severity,
            "details": details
        }
        resp = self.client.post("/api/v1/incidents", json=data)
        resp.raise_for_status()
        return resp.json()

    def registerSLO(self, service_name: str, slo_name: str, target: float) -> Dict[str, Any]:
        data = {
            "service_name": service_name,
            "slo_name": slo_name,
            "target_percentage": target
        }
        resp = self.client.post("/api/v1/slo", json=data)
        resp.raise_for_status()
        return resp.json()
