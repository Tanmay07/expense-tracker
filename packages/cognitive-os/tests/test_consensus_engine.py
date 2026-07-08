import pytest
from cognitive_os.application.consensus_engine import ConsensusEngine
from cognitive_os.domain.cognitive_models import AgentVote, AgentRole

def test_consensus_engine_unanimous():
    engine = ConsensusEngine()
    votes = [
        AgentVote(agent_role=AgentRole.BUDGET, recommendation="APPROVE_TRANSFER", confidence=0.9, rationale="Sufficient funds"),
        AgentVote(agent_role=AgentRole.RISK, recommendation="APPROVE_TRANSFER", confidence=0.8, rationale="Low risk")
    ]
    
    result = engine.evaluate_votes("msn_123", votes)
    
    assert result.achieved == True
    assert result.final_recommendation == "APPROVE_TRANSFER"
    assert result.conflict_detected == False
    assert result.escalated_to_supervisor == False

def test_consensus_engine_conflict():
    engine = ConsensusEngine()
    votes = [
        AgentVote(agent_role=AgentRole.BUDGET, recommendation="APPROVE_TRANSFER", confidence=0.9, rationale="Sufficient funds"),
        AgentVote(agent_role=AgentRole.RISK, recommendation="DENY_TRANSFER", confidence=0.85, rationale="Pattern matching fraud")
    ]
    
    result = engine.evaluate_votes("msn_123", votes)
    
    assert result.achieved == False
    assert result.conflict_detected == True
    assert result.escalated_to_supervisor == True

def test_consensus_engine_low_confidence():
    engine = ConsensusEngine()
    votes = [
        AgentVote(agent_role=AgentRole.BUDGET, recommendation="APPROVE_TRANSFER", confidence=0.4, rationale="Unsure"),
        AgentVote(agent_role=AgentRole.RISK, recommendation="APPROVE_TRANSFER", confidence=0.5, rationale="Maybe low risk")
    ]
    
    result = engine.evaluate_votes("msn_123", votes)
    
    assert result.achieved == False
    assert result.conflict_detected == False # They agree, but confidence is low
    assert result.escalated_to_supervisor == True
