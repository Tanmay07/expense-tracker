from sqlalchemy.orm import Session
from typing import Optional

from .database import DecisionCandidateModel, DecisionBundleModel
from ..domain.models import DecisionCandidate, DecisionBundle, SubScores, OpportunityCost, ConfidenceScore, EvidenceGraph, ConstraintViolation

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class CandidateRepository(BaseRepository):
    def get_by_id(self, candidate_id: str) -> Optional[DecisionCandidate]:
        record = self.db.query(DecisionCandidateModel).filter(DecisionCandidateModel.id == candidate_id).first()
        if not record:
            return None
            
        sub_scores = SubScores(**record.sub_scores) if record.sub_scores else None
        opp_cost = OpportunityCost(**record.opportunity_cost) if record.opportunity_cost else None
        conf = ConfidenceScore(**record.confidence) if record.confidence else None
        evid = EvidenceGraph(**record.evidence) if record.evidence else None
        violations = [ConstraintViolation(**v) for v in record.constraint_violations] if record.constraint_violations else []
        
        return DecisionCandidate(
            id=record.id,
            user_id=record.user_id,
            title=record.title,
            strategy=record.strategy,
            proposed_actions=record.proposed_actions,
            overall_score=record.overall_score,
            sub_scores=sub_scores,
            opportunity_cost=opp_cost,
            confidence=conf,
            evidence=evid,
            constraint_violations=violations,
            created_at=record.created_at
        )

    def save(self, candidate: DecisionCandidate) -> DecisionCandidate:
        record = DecisionCandidateModel(
            id=candidate.id,
            user_id=candidate.user_id,
            title=candidate.title,
            strategy=candidate.strategy.value,
            overall_score=candidate.overall_score,
            proposed_actions=candidate.proposed_actions,
            sub_scores=candidate.sub_scores.model_dump() if candidate.sub_scores else None,
            opportunity_cost=candidate.opportunity_cost.model_dump() if candidate.opportunity_cost else None,
            confidence=candidate.confidence.model_dump() if candidate.confidence else None,
            evidence=candidate.evidence.model_dump() if candidate.evidence else None,
            constraint_violations=[v.model_dump() for v in candidate.constraint_violations],
            created_at=candidate.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return candidate

class BundleRepository(BaseRepository):
    def save(self, bundle: DecisionBundle) -> DecisionBundle:
        record = DecisionBundleModel(
            id=bundle.id,
            user_id=bundle.user_id,
            name=bundle.name,
            combined_score=bundle.combined_score,
            candidates_json=[c.model_dump() for c in bundle.candidates],
            created_at=bundle.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return bundle
