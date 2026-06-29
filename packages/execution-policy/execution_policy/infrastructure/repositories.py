from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict, cast

from .database import PolicyModel, EvaluationLogModel
from ..domain.models import ExecutionPolicy, EvaluationResult, RuleAST

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class PolicyRepository(BaseRepository):
    def get_by_id(self, policy_id: str) -> Optional[ExecutionPolicy]:
        record = self.db.query(PolicyModel).filter(PolicyModel.id == policy_id).first()
        if not record:
            return None
            
        return ExecutionPolicy(
            id=record.id,
            name=record.name,
            description=record.description,
            category=record.category,
            version=record.version,
            priority=record.priority,
            rule_ast=RuleAST(**cast(Dict[str, Any], record.rule_ast_json)),
            outcome_if_matched=record.outcome_if_matched,
            is_active=record.is_active,
            metadata=record.metadata_json or {},
            created_at=record.created_at
        )
        
    def list_active(self) -> List[ExecutionPolicy]:
        records = self.db.query(PolicyModel).filter(PolicyModel.is_active == True).order_by(PolicyModel.priority.desc()).all()
        result = []
        for r in records:
            result.append(ExecutionPolicy(
                id=r.id,
                name=r.name,
                description=r.description,
                category=r.category,
                version=r.version,
                priority=r.priority,
                rule_ast=RuleAST(**cast(Dict[str, Any], r.rule_ast_json)),
                outcome_if_matched=r.outcome_if_matched,
                is_active=r.is_active,
                metadata=r.metadata_json or {},
                created_at=r.created_at
            ))
        return result

    def save(self, policy: ExecutionPolicy) -> ExecutionPolicy:
        record = PolicyModel(
            id=policy.id,
            name=policy.name,
            description=policy.description,
            category=policy.category.value,
            version=policy.version,
            priority=policy.priority,
            rule_ast_json=policy.rule_ast.model_dump(),
            outcome_if_matched=policy.outcome_if_matched.value,
            is_active=policy.is_active,
            metadata_json=policy.metadata,
            created_at=policy.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return policy

class EvaluationRepository(BaseRepository):
    def save(self, result: EvaluationResult) -> EvaluationResult:
        record = EvaluationLogModel(
            id=result.id,
            request_id=result.request_id,
            outcome=result.outcome.value,
            explanation_json=result.explanation.model_dump(),
            evaluated_at=result.evaluated_at
        )
        self.db.merge(record)
        self.db.commit()
        return result
