from fastapi import APIRouter, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel

from trust_platform.domain.models import (
    ConsentRecord,
    ConsentStatus,
    RiskScore,
    RiskCategory,
    AITrustRecord,
    AuditLog,
    TrustScore,
)
from trust_platform.application.services import (
    ConsentService,
    RiskService,
    AITrustService,
    AuditService,
    TrustService,
)
from trust_platform.infrastructure.database import get_db_session
from trust_platform.infrastructure.repositories import (
    ConsentRepository,
    RiskRepository,
    AITrustRepository,
    AuditRepository,
    TrustRepository,
)

router = APIRouter(prefix="/api/v1/trust", tags=["Trust & Governance"])


def get_consent_service(session=Depends(get_db_session)) -> ConsentService:
    return ConsentService(ConsentRepository(session))


def get_risk_service(session=Depends(get_db_session)) -> RiskService:
    return RiskService(RiskRepository(session))


def get_ai_trust_service(session=Depends(get_db_session)) -> AITrustService:
    return AITrustService(AITrustRepository(session))


def get_audit_service(session=Depends(get_db_session)) -> AuditService:
    return AuditService(AuditRepository(session))


def get_trust_service(session=Depends(get_db_session)) -> TrustService:
    return TrustService(TrustRepository(session))


# --- DTOs ---


class RecordConsentRequest(BaseModel):
    user_id: str
    purpose: str
    status: ConsentStatus


class LogAITrustRequest(BaseModel):
    capability_used: str
    reasoning_summary: str
    confidence: float
    safety_checks: Dict[str, bool]
    bias_evaluation: Dict[str, Any]


class EvaluateRiskRequest(BaseModel):
    target_id: str
    category: RiskCategory
    score: float


class AppendAuditLogRequest(BaseModel):
    event_type: str
    actor_id: str
    action: str
    target_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CalculateTrustScoreRequest(BaseModel):
    entity_id: str
    entity_type: str
    score: float
    factors: Dict[str, float]


# --- Routes ---


@router.post("/consent", response_model=ConsentRecord)
async def record_consent(
    req: RecordConsentRequest, svc: ConsentService = Depends(get_consent_service)
):
    return await svc.record_consent(req.user_id, req.purpose, req.status)


@router.post("/ai", response_model=AITrustRecord)
async def log_ai_execution(
    req: LogAITrustRequest, svc: AITrustService = Depends(get_ai_trust_service)
):
    return await svc.log_ai_execution(
        req.capability_used,
        req.reasoning_summary,
        req.confidence,
        req.safety_checks,
        req.bias_evaluation,
    )


@router.post("/risk", response_model=RiskScore)
async def evaluate_risk(
    req: EvaluateRiskRequest, svc: RiskService = Depends(get_risk_service)
):
    return await svc.evaluate_risk(req.target_id, req.category, req.score)


@router.post("/audit", response_model=AuditLog)
async def append_audit_log(
    req: AppendAuditLogRequest, svc: AuditService = Depends(get_audit_service)
):
    return await svc.append_audit_log(
        req.event_type, req.actor_id, req.action, req.target_id, req.metadata
    )


@router.post("/scores", response_model=TrustScore)
async def calculate_trust_score(
    req: CalculateTrustScoreRequest, svc: TrustService = Depends(get_trust_service)
):
    return await svc.calculate_trust_score(
        req.entity_id, req.entity_type, req.score, req.factors
    )
