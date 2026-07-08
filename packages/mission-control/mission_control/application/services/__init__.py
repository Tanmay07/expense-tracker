from typing import List, Dict, Any  # noqa: F401
import uuid  # noqa: F401

from ...domain.models import (
    Mission,
    MissionType,
    MissionStatus,
    MissionPriority,  # noqa: F401
    MissionExplanation,
    Opportunity,
    Risk,
    ActionTask,  # noqa: F401
)
from ...infrastructure.repositories import (
    MissionRepository,
    OpportunityRepository,
    RiskRepository,
)


class PriorityService:
    def rank_missions(self, missions: List[Mission]) -> List[Mission]:
        # Sort by urgency and financial impact
        return sorted(
            missions,
            key=lambda m: (m.priority.urgency_score, m.priority.financial_impact_score),
            reverse=True,
        )

    def resolve_conflicts(self, missions: List[Mission]) -> List[Mission]:
        # Merge duplicate recommendations logic here
        unique_missions = {}
        for m in missions:
            if m.title not in unique_missions:
                unique_missions[m.title] = m
            else:
                # Keep highest priority
                if (
                    m.priority.urgency_score
                    > unique_missions[m.title].priority.urgency_score
                ):
                    unique_missions[m.title] = m
        return list(unique_missions.values())


class MissionGeneratorService:
    def generate_from_opportunity(self, opp: Opportunity) -> Mission:
        priority = MissionPriority(
            level="MEDIUM",
            urgency_score=0.6,
            financial_impact_score=opp.score,
            confidence=0.85,
            business_impact="Revenue",
        )
        explanation = MissionExplanation(
            summary=f"Opportunity detected: {opp.title}",
            supporting_metrics={},
            timeline_events=[],
            policies_evaluated=[],
            expected_financial_benefit=opp.score * 1000,
        )
        return Mission(
            user_id=opp.user_id,
            title=opp.title,
            type=MissionType.RECOMMENDED_ACTIONS,
            priority=priority,
            explanation=explanation,
        )

    def generate_from_risk(self, risk: Risk) -> Mission:
        level = "HIGH" if risk.severity == "HIGH" else "MEDIUM"
        priority = MissionPriority(
            level=level,
            urgency_score=0.9 if level == "HIGH" else 0.5,
            financial_impact_score=0.7,
            confidence=0.9,
            business_impact="Retention",
        )
        explanation = MissionExplanation(
            summary=f"Risk detected: {risk.title}",
            supporting_metrics={},
            timeline_events=[],
            policies_evaluated=[],
            expected_financial_benefit=0.0,
        )
        return Mission(
            user_id=risk.user_id,
            title=f"Mitigate: {risk.title}",
            type=MissionType.CRITICAL_ALERTS,
            priority=priority,
            explanation=explanation,
        )


class MissionControlService:
    def __init__(
        self,
        mission_repo: MissionRepository,
        priority_service: PriorityService,
        generator: MissionGeneratorService,
    ):
        self.mission_repo = mission_repo
        self.priority_service = priority_service
        self.generator = generator

    def get_user_feed(self, user_id: str) -> List[Mission]:
        missions = self.mission_repo.get_active_by_user(user_id)
        resolved = self.priority_service.resolve_conflicts(missions)
        ranked = self.priority_service.rank_missions(resolved)
        return ranked


class OpportunityService:
    def __init__(self, repo: OpportunityRepository):
        self.repo = repo

    def detect_opportunities(self, user_id: str) -> List[Opportunity]:
        # Mock detection from AI Copilot SDKs
        opp = Opportunity(
            user_id=user_id,
            title="Increase SIP",
            description="You have excess idle cash.",
            score=0.8,
            metadata={"cash_amount": 5000},
        )
        self.repo.save(opp)
        return [opp]


class RiskService:
    def __init__(self, repo: RiskRepository):
        self.repo = repo

    def detect_risks(self, user_id: str) -> List[Risk]:
        # Mock detection
        risk = Risk(
            user_id=user_id,
            title="Subscription Waste",
            severity="LOW",
            description="You are paying for unused subscriptions.",
            metadata={"subscriptions": ["Netflix", "Gym"]},
        )
        self.repo.save(risk)
        return [risk]
