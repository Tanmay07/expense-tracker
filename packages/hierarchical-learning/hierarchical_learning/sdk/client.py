import httpx
from typing import Dict, Any, Optional

class HierarchicalLearningSDK:
    """
    SDK for the Enterprise Hierarchical Learning & Knowledge Evolution Platform (HLKEP).
    This SDK becomes the canonical intelligence layer retriever for the rest of PFOS.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)
        
    def getGlobalKnowledge(self, topic: str) -> Dict[str, Any]:
        resp = self.client.get(f"/learning/global/{topic}")
        resp.raise_for_status()
        return resp.json()
        
    def getRegionalKnowledge(self, region_id: str, topic: str) -> Dict[str, Any]:
        # Typically the router might have dedicated endpoints or we just extract from stack
        pass
        
    def getHouseholdKnowledge(self, household_id: str, topic: str) -> Dict[str, Any]:
        pass
        
    def getPersonalKnowledge(self, user_id: str, topic: str) -> Dict[str, Any]:
        pass

    def getFullKnowledgeStack(self, user_id: str, topic: str, household_id: Optional[str] = None, region_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"user_id": user_id, "topic": topic}
        if household_id:
            params["household_id"] = household_id
        if region_id:
            params["region_id"] = region_id
            
        resp = self.client.get("/learning/hierarchy/stack", params=params)
        resp.raise_for_status()
        return resp.json()

    def promoteKnowledge(self, source_scope: str, target_scope: str, source_id: str, topic: str, proposed_knowledge: dict, evidence: dict) -> dict:
        payload = {
            "source_scope": source_scope,
            "target_scope": target_scope,
            "source_id": source_id,
            "topic": topic,
            "proposed_knowledge_json": proposed_knowledge,
            "evidence_json": evidence
        }
        resp = self.client.post("/learning/promotions", json=payload)
        resp.raise_for_status()
        return resp.json()
        
    def calculateConfidence(self, sample_size: int, evidence_quality: float, behavior_stability: float) -> float:
        # Abstracted to SDK utility, could also be an API call if complex
        pass
        
    def evaluateDecay(self, topic: str, entity_id: str) -> float:
        pass
        
    def resolveConsensus(self, household_id: str, conflict_topic: str, competing_preferences: dict) -> dict:
        payload = {
            "household_id": household_id,
            "conflict_topic": conflict_topic,
            "competing_preferences_json": competing_preferences
        }
        resp = self.client.post("/learning/consensus", json=payload)
        resp.raise_for_status()
        return resp.json()
        
    def replayLearning(self, entity_id: str, topic: str, target_version: int) -> dict:
        # Not fully implemented in backend stub, placeholder for SDK contract
        pass
