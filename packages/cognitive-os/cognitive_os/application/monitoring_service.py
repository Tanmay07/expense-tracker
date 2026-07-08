from typing import Dict, Any, List
import asyncio

class ContinuousMonitoringService:
    """
    Monitors state changes across PFOS (Cash Flow, Debt, Goals, Risk).
    Triggers observation events that may lead to new missions.
    """
    def __init__(self):
        self.active_monitors = []

    async def observe_stream(self, stream_name: str, callback):
        """
        Simulates connecting to a Kafka topic or Redis stream of domain events.
        """
        self.active_monitors.append(stream_name)
        # Mocking an observation loop
        # while True:
        #     event = await fetch_event(stream_name)
        #     await callback(event)
        
    def detect_anomalies(self, current_state: Dict[str, Any], historical_baseline: Dict[str, Any]) -> List[str]:
        """
        Compares current financial state to baseline to detect anomalies.
        """
        anomalies = []
        
        # Example: Cash flow drop
        current_cash = current_state.get("available_cash", 0)
        baseline_cash = historical_baseline.get("avg_available_cash", 0)
        
        if baseline_cash > 0 and current_cash < (baseline_cash * 0.5):
            anomalies.append("SEVERE_CASH_FLOW_DROP")
            
        # Example: High Risk exposure
        if current_state.get("portfolio_volatility", 0) > 0.2:
            anomalies.append("HIGH_PORTFOLIO_VOLATILITY")
            
        return anomalies
