from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class PolicyViolation(BaseModel):
    policy_id: str
    description: str
    severity: str


class PolicyValidationResult(BaseModel):
    is_compliant: bool
    violations: List[PolicyViolation]
    modified_recommendation: Optional[str] = None


class PolicyAwareReasoningService:
    """
    Intercepts cognitive outputs (plans, recommendations) and validates them
    against the central Governance Platform and Execution Policies.
    Ensures the cognitive layer cannot bypass established business rules.
    """

    def __init__(self):
        # In production, this would be a client to the Governance Service (Phase 9)
        pass

    def validate_recommendation(
        self, agent_role: str, recommendation: str, context: Dict[str, Any]
    ) -> PolicyValidationResult:
        """
        Validates an agent's recommendation against global and agent-specific policies.
        """
        violations = []

        # Simulated Policy Check 1: Financial Constraints
        if "liquidate" in recommendation.lower() and agent_role != "SUPERVISOR":
            violations.append(
                PolicyViolation(
                    policy_id="SYS_GOV_LIQ_01",
                    description="Only the Supervisor or explicit user approval can authorize liquidation.",
                    severity="CRITICAL",
                )
            )

        # Simulated Policy Check 2: Risk Limits
        if (
            context.get("portfolio_volatility", 0) > 0.3
            and "buy options" in recommendation.lower()
        ):
            violations.append(
                PolicyViolation(
                    policy_id="FIN_RSK_05",
                    description="High volatility environment prohibits new derivatives exposure.",
                    severity="HIGH",
                )
            )

        is_compliant = len(violations) == 0

        return PolicyValidationResult(
            is_compliant=is_compliant,
            violations=violations,
            # If minor violations, the service might propose a modified compliant recommendation
            modified_recommendation=None if not is_compliant else recommendation,
        )
