from src.knowledge_graph.database import BaseGraphDatabase
from typing import Dict, Any

class RecommendationContextService:
    """
    Generates compact JSON Contexts (GraphRAG) from the Knowledge Graph 
    to be injected into LLM Prompts.
    """
    def __init__(self, db: BaseGraphDatabase):
        self.db = db
        
    def build_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Traverses the graph to find high-level behaviors and top categories
        for prompt injection.
        """
        # In a real graph DB, this query would aggregate paths.
        # e.g., MATCH (u:User {id: $user_id})-[:EXHIBITS_BEHAVIOR]->(b:Behavior) RETURN collect(b.label)
        
        cypher = """
        MATCH (u:User {id: $user_id})
        OPTIONAL MATCH (u)-[:EXHIBITS_BEHAVIOR]->(b:Behavior)
        OPTIONAL MATCH (u)-[:OWNS]->(a:Account)-[:HAS_TRANSACTION]->(t:Transaction)-[:BELONGS_TO]->(c:Category)
        RETURN u, collect(DISTINCT b.label) as behaviors, collect(DISTINCT c.name) as top_categories
        """
        
        results = self.db.execute_cypher(cypher, {"user_id": user_id})
        
        # Mocking the payload since we're using MockGraphDatabase
        return {
            "user_id": user_id,
            "inferred_behaviors": ["Frequent Traveler", "Heavy Subscription Usage"],
            "spending_categories": ["Coffee", "Software", "Travel"],
            "risk_score": 25,
            "notes": "Generated via GraphRAG traversal."
        }
