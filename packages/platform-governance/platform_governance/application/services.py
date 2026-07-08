from typing import Dict, Any


class FinOpsService:
    def __init__(self):
        self.costs = {"total_ai_tokens": 0.0, "total_db_reads": 0.0}

    def record_cost(self, resource_type: str, units: float, unit_price: float):
        total = units * unit_price
        if resource_type in self.costs:
            self.costs[resource_type] += total
        else:
            self.costs[resource_type] = total

    def get_dashboard(self) -> Dict[str, float]:
        return self.costs


class ScorecardService:
    def evaluate_package(
        self, package_name: str, has_tests: bool, has_adr: bool
    ) -> Dict[str, Any]:
        score = 0
        if has_tests:
            score += 50
        if has_adr:
            score += 50

        return {
            "package": package_name,
            "score": score,
            "status": "Enterprise Ready" if score == 100 else "Development",
        }


class PolicyService:
    def validate_ast_imports(self, file_content: str) -> bool:
        """
        Mock AST validator ensuring strict domain boundaries.
        e.g., UI cannot import Database drivers.
        """
        # If a file tries to import sqlalchemy directly instead of SDK, flag it
        if "import sqlalchemy" in file_content or "from sqlalchemy" in file_content:
            return False
        return True
