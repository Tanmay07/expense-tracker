from typing import Optional, List, Dict, Any
from datetime import datetime

from ..domain.models import (
    DecisionLifecycle,
    LifecycleState,
    ExecutionPlan,
    ExecutionStep,
    Milestone,
)
from ..infrastructure.repositories import LifecycleRepository, ExecutionPlanRepository


class DecisionLifecycleService:
    def __init__(self, repo: LifecycleRepository):
        self.repo = repo

    def initialize_lifecycle(self, decision_id: str) -> DecisionLifecycle:
        lifecycle = DecisionLifecycle(decision_id=decision_id)
        lifecycle.state_history.append(
            {
                "state": LifecycleState.GENERATED.value,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        return self.repo.save(lifecycle)

    def transition_state(
        self, decision_id: str, new_state: LifecycleState
    ) -> Optional[DecisionLifecycle]:
        lifecycle = self.repo.get_by_decision_id(decision_id)
        if not lifecycle:
            return None

        # Basic state machine validation (prevent DRAFT -> COMPLETED)
        valid_transitions = {
            LifecycleState.GENERATED: [
                LifecycleState.PENDING_REVIEW,
                LifecycleState.ARCHIVED,
            ],
            LifecycleState.PENDING_REVIEW: [
                LifecycleState.APPROVED,
                LifecycleState.REJECTED,
            ],
            LifecycleState.APPROVED: [
                LifecycleState.SCHEDULED,
                LifecycleState.IN_PROGRESS,
                LifecycleState.DEFERRED,
            ],
            LifecycleState.IN_PROGRESS: [
                LifecycleState.COMPLETED,
                LifecycleState.BLOCKED,
                LifecycleState.PAUSED,
                LifecycleState.CANCELLED,
            ],
            LifecycleState.BLOCKED: [
                LifecycleState.IN_PROGRESS,
                LifecycleState.CANCELLED,
            ],
            LifecycleState.PAUSED: [
                LifecycleState.IN_PROGRESS,
                LifecycleState.CANCELLED,
            ],
        }

        allowed = valid_transitions.get(lifecycle.current_state, [])
        if new_state not in allowed:
            raise ValueError(
                f"Invalid transition from {lifecycle.current_state} to {new_state}"
            )

        lifecycle.current_state = new_state
        lifecycle.state_history.append(
            {"state": new_state.value, "timestamp": datetime.utcnow().isoformat()}
        )
        return self.repo.save(lifecycle)


class ExecutionPlannerService:
    def __init__(self, repo: ExecutionPlanRepository):
        self.repo = repo

    def generate_plan(
        self, decision_id: str, proposed_actions: List[Dict[str, Any]]
    ) -> ExecutionPlan:
        steps = []
        for action in proposed_actions:
            steps.append(
                ExecutionStep(
                    description=f"Execute {action.get('type')}",
                    is_automated=True,
                    required_funds=action.get("amount", 0.0),
                )
            )

        milestones = [Milestone(name="Initialization", description="Setup complete")]

        plan = ExecutionPlan(
            decision_id=decision_id,
            steps=steps,
            milestones=milestones,
            estimated_duration_days=5,
        )
        return self.repo.save(plan)
