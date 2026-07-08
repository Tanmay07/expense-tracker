from cognitive_os.application.consensus_engine import ConsensusEngine
from cognitive_os.domain.cognitive_models import AgentVote, AgentRole
from cognitive_os.infrastructure.redis_store import TransientStateStore
from cognitive_os.infrastructure.db import DurablePostgresRepository


def get_engine():
    return ConsensusEngine(DurablePostgresRepository(), TransientStateStore())


def test_consensus_engine_unanimous():
    engine = get_engine()
    votes = [
        AgentVote(
            agent_role=AgentRole.BUDGET,
            recommendation="APPROVE_TRANSFER",
            confidence=0.9,
            rationale="Sufficient funds",
        ),
        AgentVote(
            agent_role=AgentRole.RISK,
            recommendation="APPROVE_TRANSFER",
            confidence=0.8,
            rationale="Low risk",
        ),
    ]

    result = engine.evaluate_votes("msn_123", votes)

    assert result.achieved
    assert result.final_recommendation == "APPROVE_TRANSFER"
    assert not result.conflict_detected
    assert not result.escalated_to_supervisor


def test_consensus_engine_conflict():
    engine = get_engine()
    votes = [
        AgentVote(
            agent_role=AgentRole.BUDGET,
            recommendation="APPROVE_TRANSFER",
            confidence=0.9,
            rationale="Sufficient funds",
        ),
        AgentVote(
            agent_role=AgentRole.RISK,
            recommendation="DENY_TRANSFER",
            confidence=0.85,
            rationale="Pattern matching fraud",
        ),
    ]

    result = engine.evaluate_votes("msn_123", votes)

    assert not result.achieved
    assert result.conflict_detected
    assert result.escalated_to_supervisor


def test_consensus_engine_low_confidence():
    engine = get_engine()
    votes = [
        AgentVote(
            agent_role=AgentRole.BUDGET,
            recommendation="APPROVE_TRANSFER",
            confidence=0.4,
            rationale="Unsure",
        ),
        AgentVote(
            agent_role=AgentRole.RISK,
            recommendation="APPROVE_TRANSFER",
            confidence=0.5,
            rationale="Maybe low risk",
        ),
    ]

    result = engine.evaluate_votes("msn_123", votes)

    assert not result.achieved
    assert not result.conflict_detected  # They agree, but confidence is low
    assert result.escalated_to_supervisor
