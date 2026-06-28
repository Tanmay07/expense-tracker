from typing import Dict, Any, List

class LineageService:
    def __init__(self):
        # A simple in-memory tracker mapping metric requests to data sources
        self.traces: Dict[str, Dict[str, Any]] = {}
        
    def record_trace(self, query_id: str, metric_id: str, dependencies: List[str], data_sources: List[str]):
        self.traces[query_id] = {
            "metric": metric_id,
            "dependencies_resolved": dependencies,
            "raw_tables_scanned": data_sources
        }

    def get_lineage(self, query_id: str) -> Dict[str, Any]:
        return self.traces.get(query_id)

class CalculationGraphEngine:
    def __init__(self, lineage: LineageService):
        self.lineage = lineage
        # Hardcoded DAG definitions for the prototype
        self.dag = {
            "savings_rate": {
                "depends_on": ["savings", "income"],
                "formula": "savings / income"
            },
            "savings": {
                "depends_on": ["income", "expenses"],
                "formula": "income - expenses"
            },
            "income": {
                "depends_on": ["raw_ledger_credits"],
                "formula": "sum(credits)"
            },
            "expenses": {
                "depends_on": ["raw_ledger_debits"],
                "formula": "sum(debits)"
            }
        }
        
    def resolve_metric(self, metric_id: str, raw_data: Dict[str, float]) -> float:
        """
        Recursively resolves a metric by traversing the DAG.
        """
        import uuid
        query_id = str(uuid.uuid4())
        
        def _evaluate(node: str) -> float:
            if node == "income":
                return raw_data.get("income", 0.0)
            if node == "expenses":
                return raw_data.get("expenses", 0.0)
            if node == "savings":
                i = _evaluate("income")
                e = _evaluate("expenses")
                return i - e
            if node == "savings_rate":
                s = _evaluate("savings")
                i = _evaluate("income")
                if i == 0:
                    return 0.0
                return s / i
            raise ValueError(f"Unknown metric {node}")
            
        result = _evaluate(metric_id)
        
        # Determine dependencies for lineage
        deps = self.dag.get(metric_id, {}).get("depends_on", [])
        self.lineage.record_trace(query_id, metric_id, deps, ["postgres.ledger_entries"])
        
        return result, query_id
