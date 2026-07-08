from typing import List, Optional
from pydantic import BaseModel, Field
from .models import AgentRole

class AgentVote(BaseModel):
    agent_role: AgentRole
    recommendation: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str

class ConsensusResult(BaseModel):
    mission_id: str
    achieved: bool
    final_recommendation: Optional[str]
    confidence_score: float
    conflict_detected: bool
    votes: List[AgentVote]
    escalated_to_supervisor: bool = False

class ReflectionResult(BaseModel):
    mission_id: str
    success_score: float = Field(..., ge=0.0, le=1.0)
    predicted_impact: float
    actual_impact: float
    lessons_learned: List[str]
    improvement_recommendations: List[str]
    timestamp: str
