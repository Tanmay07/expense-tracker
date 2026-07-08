from typing import Optional, Dict, Any
import uuid

from trust_platform.domain.models import (
    ConsentRecord,
    ConsentStatus,
    AITrustRecord,
    RiskScore,
    RiskCategory,
    AuditLog,
    TrustScore,
)
from trust_platform.infrastructure.database import (
    ConsentRecordModel,
    AITrustRecordModel,
    RiskScoreModel,
    AuditLogModel,
    TrustScoreModel,
)
from trust_platform.infrastructure.repositories import (
    ConsentRepository,
    AITrustRepository,
    RiskRepository,
    AuditRepository,
    TrustRepository,
)
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class ConsentService:
    def __init__(self, repo: ConsentRepository):
        self.repo = repo

    @tracer.start_as_current_span("record_consent")
    async def record_consent(
        self, user_id: str, purpose: str, status: ConsentStatus
    ) -> ConsentRecord:
        db_model = ConsentRecordModel(
            id=str(uuid.uuid4()), user_id=user_id, purpose=purpose, status=status
        )
        await self.repo.record_consent(db_model)
        return ConsentRecord(
            id=db_model.id,
            user_id=db_model.user_id,
            purpose=db_model.purpose,
            status=db_model.status,
            version=db_model.version,
            granted_at=db_model.granted_at,
            expires_at=db_model.expires_at,
        )

    @tracer.start_as_current_span("check_consent")
    async def check_consent(self, user_id: str, purpose: str) -> bool:
        record = await self.repo.get_active_consent(user_id, purpose)
        return record is not None


class AITrustService:
    def __init__(self, repo: AITrustRepository):
        self.repo = repo

    @tracer.start_as_current_span("log_ai_execution")
    async def log_ai_execution(
        self,
        capability_used: str,
        reasoning_summary: str,
        confidence: float,
        safety_checks: Dict[str, bool],
        bias_evaluation: Dict[str, Any],
    ) -> AITrustRecord:
        record_model = AITrustRecordModel(
            id=str(uuid.uuid4()),
            capability_used=capability_used,
            reasoning_summary=reasoning_summary,
            confidence=confidence,
            safety_checks=safety_checks,
            bias_evaluation=bias_evaluation,
        )
        await self.repo.log_ai_execution(record_model)
        return AITrustRecord(
            id=record_model.id,
            capability_used=record_model.capability_used,
            reasoning_summary=record_model.reasoning_summary,
            confidence=record_model.confidence,
            safety_checks=record_model.safety_checks,
            bias_evaluation=record_model.bias_evaluation,
            approval_required=record_model.approval_required,
            executed_at=record_model.executed_at,
        )


class RiskService:
    def __init__(self, repo: RiskRepository):
        self.repo = repo

    @tracer.start_as_current_span("evaluate_risk")
    async def evaluate_risk(
        self, target_id: str, category: RiskCategory, score: float
    ) -> RiskScore:
        risk_model = RiskScoreModel(
            id=str(uuid.uuid4()), target_id=target_id, category=category, score=score
        )
        await self.repo.save_risk_score(risk_model)
        return RiskScore(
            id=risk_model.id,
            target_id=risk_model.target_id,
            category=risk_model.category,
            score=risk_model.score,
            evaluated_at=risk_model.evaluated_at,
        )


class AuditService:
    def __init__(self, repo: AuditRepository):
        self.repo = repo

    @tracer.start_as_current_span("append_audit_log")
    async def append_audit_log(
        self,
        event_type: str,
        actor_id: str,
        action: str,
        target_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        log_model = AuditLogModel(
            id=str(uuid.uuid4()),
            event_type=event_type,
            actor_id=actor_id,
            target_id=target_id,
            action=action,
            metadata_json=metadata or {},
        )
        await self.repo.append_audit_log(log_model)
        return AuditLog(
            id=log_model.id,
            event_type=log_model.event_type,
            actor_id=log_model.actor_id,
            target_id=log_model.target_id,
            action=log_model.action,
            timestamp=log_model.timestamp,
            metadata=log_model.metadata_json,
            is_immutable=log_model.is_immutable,
        )


class TrustService:
    def __init__(self, repo: TrustRepository):
        self.repo = repo

    @tracer.start_as_current_span("calculate_trust_score")
    async def calculate_trust_score(
        self, entity_id: str, entity_type: str, score: float, factors: Dict[str, float]
    ) -> TrustScore:
        score_model = TrustScoreModel(
            id=str(uuid.uuid4()),
            entity_id=entity_id,
            entity_type=entity_type,
            score=score,
            factors=factors,
        )
        await self.repo.save_trust_score(score_model)
        return TrustScore(
            id=score_model.id,
            entity_id=score_model.entity_id,
            entity_type=score_model.entity_type,
            score=score_model.score,
            factors=score_model.factors,
            evaluated_at=score_model.evaluated_at,
        )


class ComplianceService:
    pass


class PrivacyService:
    pass


class GovernanceService:
    pass


class EvidenceService:
    pass
