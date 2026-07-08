from typing import List, Dict, Any
from ..domain.cognitive_models import AgentVote, ConsensusResult
import collections

class ConsensusEngine:
    """
    Evaluates recommendations from multiple agents, weighting their confidence
    and detecting conflicts before execution.
    """
    
    def evaluate_votes(self, mission_id: str, votes: List[AgentVote]) -> ConsensusResult:
        if not votes:
            return ConsensusResult(
                mission_id=mission_id, achieved=False, final_recommendation=None,
                confidence_score=0.0, conflict_detected=True, votes=[], escalated_to_supervisor=True
            )

        # Group recommendations
        recommendation_scores = collections.defaultdict(float)
        
        for vote in votes:
            # Simple weighted score based on confidence
            recommendation_scores[vote.recommendation] += vote.confidence

        # Sort by highest score
        sorted_recommendations = sorted(recommendation_scores.items(), key=lambda item: item[1], reverse=True)
        
        top_rec, top_score = sorted_recommendations[0]
        
        # Check for conflicts (if top 2 are very close in score)
        conflict_detected = False
        if len(sorted_recommendations) > 1:
            runner_up_rec, runner_up_score = sorted_recommendations[1]
            if (top_score - runner_up_score) < 0.2: # Threshold for conflict
                conflict_detected = True

        # Calculate average confidence
        avg_confidence = sum(v.confidence for v in votes) / len(votes)
        
        # If confidence is too low or conflict is high, escalate
        escalated = conflict_detected or (avg_confidence < 0.6)
        
        return ConsensusResult(
            mission_id=mission_id,
            achieved=not escalated,
            final_recommendation=top_rec if not escalated else None,
            confidence_score=avg_confidence,
            conflict_detected=conflict_detected,
            votes=votes,
            escalated_to_supervisor=escalated
        )
