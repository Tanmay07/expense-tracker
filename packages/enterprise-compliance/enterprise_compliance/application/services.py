from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import uuid

from ..domain.models import (
    RiskProfile, CompliancePolicy, SuitabilityProfile, 
    InvestmentConstraint, DecisionRecord, DecisionStatus, PolicySeverity
)
from ..infrastructure.repositories import (
    RiskProfileRepository, PolicyRepository, SuitabilityRepository,
    ConstraintRepository, DecisionRepository
)

class EvaluationResult(BaseModel):
    is_compliant: bool
    violations: List[str]
    warnings: List[str]
    confidence_score: float

class SuitabilityService:
    def __init__(self, repository: SuitabilityRepository, risk_repo: RiskProfileRepository):
        self.repository = repository
        self.risk_repo = risk_repo

    def evaluate_suitability(self, user_id: str, investment_params: Dict[str, Any]) -> SuitabilityProfile:
        # Complex logic to evaluate suitability based on RiskProfile and Investment Params
        risk_profile = self.risk_repo.get_by_user_id(user_id)
        if not risk_profile:
            raise ValueError("User Risk Profile not found")
            
        score = 85.0 # Mock calculation
        confidence = 0.95
        
        profile = SuitabilityProfile(
            user_id=user_id,
            suitability_score=score,
            confidence_score=confidence,
            factors={"risk_match": True, "horizon_match": True}
        )
        return self.repository.save(profile)

class ComplianceService:
    def __init__(self, policy_repo: PolicyRepository, decision_repo: DecisionRepository):
        self.policy_repo = policy_repo
        self.decision_repo = decision_repo

    def evaluate_transaction(self, user_id: str, context_id: str, transaction_data: Dict[str, Any]) -> EvaluationResult:
        policies = self.policy_repo.get_active_policies()
        violations = []
        warnings = []
        
        for policy in policies:
            # Mock evaluation logic
            if policy.name == "Maximum Crypto Exposure" and transaction_data.get("asset_class") == "CRYPTO":
                violations.append(policy.id)
                
        status = DecisionStatus.REJECTED if violations else DecisionStatus.APPROVED
        
        decision = DecisionRecord(
            context_id=context_id,
            action_type="TRANSACTION_EVALUATION",
            status=status,
            confidence=0.99,
            policies_evaluated=[p.id for p in policies],
            rules_triggered=violations,
            explanation=f"Evaluated {len(policies)} policies. Status: {status.value}"
        )
        self.decision_repo.save(decision)
        
        return EvaluationResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            confidence_score=0.99
        )

class PolicyService:
    def __init__(self, repository: PolicyRepository):
        self.repository = repository

    def create_policy(self, policy_data: dict) -> CompliancePolicy:
        policy = CompliancePolicy(**policy_data)
        return self.repository.save(policy)
        
    def get_active_policies(self) -> List[CompliancePolicy]:
        return self.repository.get_active_policies()

class ExplainabilityService:
    def __init__(self, decision_repo: DecisionRepository):
        self.decision_repo = decision_repo

    def explain_decision(self, context_id: str) -> Dict[str, Any]:
        records = self.decision_repo.get_by_context_id(context_id)
        if not records:
            return {"error": "Decision context not found"}
        
        latest_record = records[-1]
        
        return {
            "decision_id": latest_record.id,
            "status": latest_record.status.value,
            "explanation_narrative": latest_record.explanation,
            "policies_evaluated_count": len(latest_record.policies_evaluated),
            "confidence": latest_record.confidence
        }
