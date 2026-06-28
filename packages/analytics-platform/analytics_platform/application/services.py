from typing import Dict, Any, List

class MetricRegistryService:
    def __init__(self):
        # Metric ID -> Definition
        self.metrics: Dict[str, Dict[str, Any]] = {}
        
    def register_metric(self, metric_id: str, name: str, formula: str, units: str, owner: str):
        self.metrics[metric_id] = {
            "name": name,
            "formula": formula, # e.g. "(Income - Expenses) / Income"
            "units": units,
            "owner": owner,
            "version": "1.0"
        }
        return metric_id

    def get_metric_definition(self, metric_id: str) -> Dict[str, Any]:
        return self.metrics.get(metric_id)

class AnalyticsService:
    def __init__(self, registry: MetricRegistryService):
        self.registry = registry
        
    def evaluate_metric(self, user_id: str, metric_id: str, raw_data: Dict[str, float]) -> float:
        definition = self.registry.get_metric_definition(metric_id)
        if not definition:
            raise ValueError(f"Metric {metric_id} not found in Semantic Registry")
            
        # In a real system, we'd use DuckDB/Polars or safely evaluate an AST against the Data Warehouse.
        # For this prototype, we'll implement hardcoded fallbacks to demonstrate the routing concept safely.
        if metric_id == "savings_rate":
            income = raw_data.get("income", 0.0)
            expenses = raw_data.get("expenses", 0.0)
            if income == 0:
                return 0.0
            return (income - expenses) / income
            
        if metric_id == "debt_to_income":
            income = raw_data.get("income", 0.0)
            debt_payments = raw_data.get("debt_payments", 0.0)
            if income == 0:
                return 0.0
            return debt_payments / income
            
        raise NotImplementedError(f"Evaluation for {metric_id} is not implemented in prototype engine")
