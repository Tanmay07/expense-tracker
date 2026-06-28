from typing import Dict, Any, List
import uuid
import random

class ScenarioEngine:
    def __init__(self):
        # Scenario ID -> Scenario Definition
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        
    def create_scenario(self, user_id: str, name: str, events: List[Dict[str, Any]]) -> str:
        scenario_id = str(uuid.uuid4())
        self.scenarios[scenario_id] = {
            "user_id": user_id,
            "name": name,
            "injected_events": events
        }
        return scenario_id

    def get_scenario(self, scenario_id: str) -> Dict[str, Any]:
        return self.scenarios.get(scenario_id)

class MonteCarloEngine:
    def __init__(self, scenario_engine: ScenarioEngine):
        self.scenario_engine = scenario_engine
        
    def run_simulation(self, scenario_id: str, current_portfolio_value: float, years: int = 10, iterations: int = 1000):
        scenario = self.scenario_engine.get_scenario(scenario_id)
        if not scenario:
            raise ValueError("Scenario not found")
            
        # Extract constraints from injected events (e.g. -50000 for a house purchase in year 1)
        # Mocking complex matrix operations with basic python math for rapid prototyping
        
        final_values = []
        for _ in range(iterations):
            value = current_portfolio_value
            for year in range(years):
                # Random return between -10% and +20%
                annual_return = random.uniform(-0.10, 0.20)
                value = value * (1 + annual_return)
                
                # Apply scenario events
                for event in scenario["injected_events"]:
                    if event.get("year") == year:
                        if event["type"] == "EXPENSE":
                            value -= event["amount"]
                        elif event["type"] == "INCOME":
                            value += event["amount"]
                            
            final_values.append(value)
            
        final_values.sort()
        p10 = final_values[int(iterations * 0.1)]
        p50 = final_values[int(iterations * 0.5)]
        p90 = final_values[int(iterations * 0.9)]
        
        return {
            "scenario_id": scenario_id,
            "iterations": iterations,
            "years": years,
            "p10_worst_case": p10,
            "p50_expected": p50,
            "p90_best_case": p90
        }
