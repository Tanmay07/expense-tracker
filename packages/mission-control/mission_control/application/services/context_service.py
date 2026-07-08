from typing import List, Dict, Any
from datetime import datetime
from ...domain.models.context import (
    FinancialContext,
    ContextCard,
    AdaptiveAction,
    ContextExplanation,
    ContextPriority,
    ContextCardType,
)


class ContextWorkspaceService:
    def get_active_contexts(self, user_id: str) -> List[FinancialContext]:
        # In a real system, this would query the Decision Engine and Knowledge Graph
        # We will mock the output to simulate adaptive responses

        return [
            FinancialContext(
                id="ctx-debt-1",
                name="High Credit Card Utilization",
                active=True,
                priority=ContextPriority.CRITICAL,
                confidence=96,
                impact_score=85,
                urgency=90,
                recommended_mission_id="m-debt-payoff",
                detected_at=datetime.utcnow(),
                explanation=ContextExplanation(
                    reason="Credit utilization is 81%.",
                    expected_impact="Completing this mission could save approximately $1,500 annually in interest.",
                    recommended_action="Execute immediate transfer to high-interest accounts.",
                    confidence_score=96,
                    supporting_evidence=[
                        "Chase Sapphire balance is $12,450 / $15,000 limit.",
                        "Average daily interest charge is $8.45.",
                    ],
                ),
                cards=[
                    ContextCard(
                        id="card-1",
                        card_type=ContextCardType.DEBT_ALERT,
                        title="Critical Debt Level Detected",
                        description="Your credit utilization is harming your credit score and costing you daily interest.",
                        priority=ContextPriority.CRITICAL,
                        explanation=ContextExplanation(
                            reason="Utilization > 80%",
                            expected_impact="Credit score drop of ~40 points",
                            recommended_action="Pay down $5,000",
                            confidence_score=99,
                            supporting_evidence=[
                                "Equifax rules",
                                "Current balance ratio",
                            ],
                        ),
                        actions=[
                            AdaptiveAction(
                                id="act-1",
                                label="Review Debt Mission",
                                action_type="NAVIGATE",
                                icon="Target",
                                payload={"route": "/missions/m-debt-payoff"},
                                primary=True,
                            )
                        ],
                        data={"utilization": 81, "balance": 12450},
                    )
                ],
            )
        ]


class AdaptiveDashboardService:
    def get_dashboard_layout(
        self, user_id: str, contexts: List[FinancialContext]
    ) -> Dict[str, Any]:
        # Dynamically arrange widgets based on active contexts
        layout = {
            "top_section": "active_mission"
            if any(c.priority == ContextPriority.CRITICAL for c in contexts)
            else "metrics",
            "widgets": [],
            "pinned_cards": [],
        }

        for ctx in contexts:
            layout["pinned_cards"].extend(ctx.cards)

        layout["widgets"] = ["cash_flow", "recent_transactions", "ai_priorities"]
        return layout


class AdaptiveActionService:
    def get_quick_actions(
        self, user_id: str, contexts: List[FinancialContext]
    ) -> List[AdaptiveAction]:
        actions = []
        if any(c.name == "High Credit Card Utilization" for c in contexts):
            actions.append(
                AdaptiveAction(
                    id="qa-pay-debt",
                    label="Pay EMI",
                    action_type="EXECUTE_TRANSFER",
                    icon="CreditCard",
                    payload={"target": "debt"},
                    primary=True,
                )
            )
        actions.append(
            AdaptiveAction(
                id="qa-ask-ai",
                label="Ask AI",
                action_type="OPEN_COPILOT",
                icon="Bot",
                payload={},
                primary=False,
            )
        )
        return actions


class MissionPrioritizationService:
    def get_prioritized_missions(self, user_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "id": "m-debt-payoff",
                "title": "Credit Card Payoff",
                "priority_score": 95,
                "status": "ACTIVE",
            },
            {
                "id": "m-tax-harvest",
                "title": "Tax Loss Harvesting",
                "priority_score": 80,
                "status": "PAUSED",
            },
        ]
