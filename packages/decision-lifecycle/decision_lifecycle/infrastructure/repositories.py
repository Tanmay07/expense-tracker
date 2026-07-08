from sqlalchemy.orm import Session
from typing import Optional

from .database import DecisionLifecycleModel, ExecutionPlanModel, ObjectiveModel
from ..domain.models import DecisionLifecycle, ExecutionPlan, FinancialObjective, ExecutionStep, Milestone, RollbackPlan

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class LifecycleRepository(BaseRepository):
    def get_by_decision_id(self, decision_id: str) -> Optional[DecisionLifecycle]:
        record = self.db.query(DecisionLifecycleModel).filter(DecisionLifecycleModel.decision_id == decision_id).first()
        if not record:
            return None
            
        return DecisionLifecycle(
            id=record.id,
            decision_id=record.decision_id,
            current_state=record.current_state,
            state_history=record.state_history,
            objective_id=record.objective_id,
            execution_plan_id=record.execution_plan_id,
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    def save(self, lifecycle: DecisionLifecycle) -> DecisionLifecycle:
        record = DecisionLifecycleModel(
            id=lifecycle.id,
            decision_id=lifecycle.decision_id,
            current_state=lifecycle.current_state.value,
            state_history=lifecycle.state_history,
            objective_id=lifecycle.objective_id,
            execution_plan_id=lifecycle.execution_plan_id,
            created_at=lifecycle.created_at,
            updated_at=lifecycle.updated_at
        )
        self.db.merge(record)
        self.db.commit()
        return lifecycle

class ExecutionPlanRepository(BaseRepository):
    def get_by_decision_id(self, decision_id: str) -> Optional[ExecutionPlan]:
        record = self.db.query(ExecutionPlanModel).filter(ExecutionPlanModel.decision_id == decision_id).first()
        if not record:
            return None
            
        steps = [ExecutionStep(**s) for s in record.steps_json] if record.steps_json else []
        milestones = [Milestone(**m) for m in record.milestones_json] if record.milestones_json else []
        rollback = RollbackPlan(**record.rollback_plan_json) if record.rollback_plan_json else None
        
        return ExecutionPlan(
            id=record.id,
            decision_id=record.decision_id,
            steps=steps,
            milestones=milestones,
            rollback_plan=rollback,
            estimated_duration_days=record.estimated_duration_days,
            created_at=record.created_at
        )
        
    def save(self, plan: ExecutionPlan) -> ExecutionPlan:
        record = ExecutionPlanModel(
            id=plan.id,
            decision_id=plan.decision_id,
            steps_json=[s.model_dump() for s in plan.steps],
            milestones_json=[m.model_dump() for m in plan.milestones],
            rollback_plan_json=plan.rollback_plan.model_dump() if plan.rollback_plan else None,
            estimated_duration_days=plan.estimated_duration_days,
            created_at=plan.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return plan

class ObjectiveRepository(BaseRepository):
    def save(self, objective: FinancialObjective) -> FinancialObjective:
        record = ObjectiveModel(
            id=objective.id,
            canonical_name=objective.canonical_name,
            category=objective.category.value,
            weight=objective.weight,
            target_value=objective.target_value,
            current_value=objective.current_value,
            metadata_json=objective.metadata
        )
        self.db.merge(record)
        self.db.commit()
        return objective
