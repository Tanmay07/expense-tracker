from typing import List, Optional, Dict, Any

from ..domain.models import DecisionCandidate, OpportunityCost, SubScores
from ..infrastructure.repositories import CandidateRepository


class OptimizationService:
    def __init__(self, repo: CandidateRepository):
        self.repo = repo

    def generate_candidates(
        self, user_id: str, profile_data: Dict[str, Any]
    ) -> List[DecisionCandidate]:
        """
        Mock multi-objective optimization using a simple heuristic proxy
        representing OR-Tools / SciPy underlying execution.
        """
        # In a real environment, this builds a constraint model using `ortools`
        # and outputs Pareto-optimal points across Net Worth vs Liquidity vs Risk

        c1 = DecisionCandidate(
            user_id=user_id,
            title="Aggressive Debt Paydown",
            strategy="DEBT_FIRST",
            proposed_actions=[{"type": "pay_debt", "amount": 5000}],
            overall_score=85.5,
            sub_scores=SubScores(
                financial_impact=90,
                risk=20,
                urgency=80,
                goal_alignment=85,
                liquidity_impact=-50,
            ),
        )

        c2 = DecisionCandidate(
            user_id=user_id,
            title="Balanced Liquidity Retention",
            strategy="LIQUIDITY_FIRST",
            proposed_actions=[
                {"type": "save", "amount": 2500},
                {"type": "pay_debt", "amount": 2500},
            ],
            overall_score=82.0,
            sub_scores=SubScores(
                financial_impact=70,
                risk=10,
                urgency=50,
                goal_alignment=80,
                liquidity_impact=10,
            ),
        )

        self.repo.save(c1)
        self.repo.save(c2)
        return [c1, c2]


class OpportunityCostService:
    def __init__(self, repo: CandidateRepository):
        self.repo = repo

    def calculate_cost(self, candidate_id: str) -> Optional[DecisionCandidate]:
        candidate = self.repo.get_by_id(candidate_id)
        if not candidate:
            return None

        # Mock calculation of future value compounding
        future_val = (
            sum(a.get("amount", 0) for a in candidate.proposed_actions) * 1.05**10
        )

        candidate.opportunity_cost = OpportunityCost(
            future_value=future_val,
            goal_delay_months=3,
            alternative_investment_yield=5.0,
            explanation=f"If invested at 5% for 10 years, yields {future_val}",
        )
        return self.repo.save(candidate)
