from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseGraphDatabase(ABC):
    @abstractmethod
    def execute_cypher(self, query: str, parameters: dict = None) -> List[Dict[str, Any]]:
        pass

class MockGraphDatabase(BaseGraphDatabase):
    """
    Since Apache AGE or Neo4j requires heavy docker setups, we mock the graph execution 
    for the architectural scaffolding. This captures the cypher queries that would be executed.
    """
    def __init__(self):
        self.execution_log = []
        
    def execute_cypher(self, query: str, parameters: dict = None) -> List[Dict[str, Any]]:
        self.execution_log.append({
            "query": query,
            "parameters": parameters or {}
        })
        # Simulate returning empty nodes
        return []
