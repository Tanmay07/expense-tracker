from typing import Optional, List, Dict, Any

from ..domain.models import (
    ExecutionPolicy, 
    PolicyContext, 
    EvaluationResult, 
    EvaluationOutcome,
    RuleAST,
    RuleOperator,
    PolicyExplanation
)
from ..infrastructure.repositories import PolicyRepository, EvaluationRepository

class ASTEvaluator:
    @staticmethod
    def _get_field_value(context: PolicyContext, field_path: str) -> Any:
        # Simplistic dot-notation field resolver
        # e.g. "decision_metadata.amount"
        parts = field_path.split(".")
        current = context.model_dump()
        for p in parts:
            if isinstance(current, dict) and p in current:
                current = current[p]
            else:
                return None
        return current

    @staticmethod
    def evaluate(ast: RuleAST, context: PolicyContext) -> bool:
        if ast.operator == RuleOperator.AND:
            return all(ASTEvaluator.evaluate(cond, context) for cond in (ast.conditions or []))
        if ast.operator == RuleOperator.OR:
            return any(ASTEvaluator.evaluate(cond, context) for cond in (ast.conditions or []))
            
        field_val = ASTEvaluator._get_field_value(context, ast.field)
        
        if ast.operator == RuleOperator.EQ:
            return field_val == ast.value
        if ast.operator == RuleOperator.NEQ:
            return field_val != ast.value
        if ast.operator == RuleOperator.GT:
            return field_val is not None and field_val > ast.value
        if ast.operator == RuleOperator.LT:
            return field_val is not None and field_val < ast.value
        if ast.operator == RuleOperator.GTE:
            return field_val is not None and field_val >= ast.value
        if ast.operator == RuleOperator.LTE:
            return field_val is not None and field_val <= ast.value
        if ast.operator == RuleOperator.IN:
            return field_val is not None and field_val in (ast.value or [])
            
        return False

class PolicyRegistryService:
    def __init__(self, repo: PolicyRepository):
        self.repo = repo

    def register_policy(self, policy: ExecutionPolicy) -> ExecutionPolicy:
        return self.repo.save(policy)

    def list_active_policies(self) -> List[ExecutionPolicy]:
        return self.repo.list_active()

class PolicyEvaluationService:
    def __init__(self, policy_repo: PolicyRepository, eval_repo: EvaluationRepository):
        self.policy_repo = policy_repo
        self.eval_repo = eval_repo
        
    def evaluate(self, context: PolicyContext) -> EvaluationResult:
        policies = self.policy_repo.list_active()
        
        # Default outcome if no policies match
        outcome = EvaluationOutcome.ALLOW
        triggering_policy = None
        matched_conditions = []
        
        # Policies are assumed to be sorted by priority desc
        for policy in policies:
            is_match = ASTEvaluator.evaluate(policy.rule_ast, context)
            if is_match:
                outcome = policy.outcome_if_matched
                triggering_policy = policy
                matched_conditions.append(f"Matched rule tree for field: {policy.rule_ast.field if policy.rule_ast.field else 'complex'}")
                break # First match wins in this simple priority model
                
        explanation = PolicyExplanation(
            triggering_policy_id=triggering_policy.id if triggering_policy else None,
            triggering_policy_name=triggering_policy.name if triggering_policy else "Default Allow",
            matched_conditions=matched_conditions,
            human_readable=f"Execution is {outcome.value} due to {triggering_policy.name if triggering_policy else 'default policy'}."
        )
        
        result = EvaluationResult(
            request_id=context.request_id,
            outcome=outcome,
            explanation=explanation
        )
        
        self.eval_repo.save(result)
        return result
