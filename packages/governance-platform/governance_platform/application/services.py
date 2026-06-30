import uuid
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any

from governance_platform.domain.models import (
    GovernancePolicy, GovernancePolicyCreate, TrustScore, MaturityRecord,
    AIGovernanceRecord, AIGovernanceRecordCreate, EvidenceLedgerEntry, WorkflowState
)
from governance_platform.infrastructure.repositories import (
    PolicyRepository, TrustRepository, MaturityRepository,
    AIGovernanceRepository, EvidenceRepository, WorkflowRepository
)


class GovernancePolicyService:
    def __init__(self, repo: PolicyRepository):
        self.repo = repo
        
    def declare_policy(self, dto: GovernancePolicyCreate) -> GovernancePolicy:
        policy = GovernancePolicy(
            id=f"pol_{uuid.uuid4().hex}",
            name=dto.name,
            description=dto.description,
            domain=dto.domain,
            version=dto.version,
            policy_payload_json=dto.policy_payload_json,
            status="ACTIVE",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return self.repo.save(policy)


class TrustService:
    def __init__(self, repo: TrustRepository):
        self.repo = repo
        
    def calculate_trust(self, asset_id: str) -> TrustScore:
        # Fetch existing or create new
        score = self.repo.get_by_asset(asset_id)
        if not score:
            score = TrustScore(
                id=f"trust_{uuid.uuid4().hex}",
                asset_id=asset_id,
                last_calculated_at=datetime.utcnow()
            )
            
        # Simplified trust algorithm based on spec weights
        # Assume these metrics are updated asynchronously by the Celery tasks
        composite = (
            (score.validation_score * 0.3) +
            (score.policy_compliance_score * 0.3) +
            (score.ai_confidence_score * 0.2) +
            (score.lineage_score * 0.2)
        )
        
        score.composite_trust_score = composite
        score.is_trusted = composite >= 80.0
        score.last_calculated_at = datetime.utcnow()
        
        return self.repo.save(score)


class MaturityService:
    def __init__(self, repo: MaturityRepository):
        self.repo = repo
        
    def promote_asset(self, asset_id: str, new_level: str, promoted_by: str, reason: str) -> MaturityRecord:
        record = self.repo.get_by_asset(asset_id)
        if not record:
            record = MaturityRecord(
                id=f"mat_{uuid.uuid4().hex}",
                asset_id=asset_id,
                current_level=new_level,
                promoted_at=datetime.utcnow(),
                promoted_by=promoted_by,
                reason=reason
            )
        else:
            record.current_level = new_level
            record.promoted_at = datetime.utcnow()
            record.promoted_by = promoted_by
            record.reason = reason
            
        return self.repo.save(record)


class AIGovernanceService:
    def __init__(self, repo: AIGovernanceRepository):
        self.repo = repo
        
    def record_metrics(self, dto: AIGovernanceRecordCreate) -> AIGovernanceRecord:
        record = AIGovernanceRecord(
            id=f"aim_{uuid.uuid4().hex}",
            asset_id=dto.asset_id,
            hallucination_rate=dto.hallucination_rate,
            bias_score=dto.bias_score,
            fairness_score=dto.fairness_score,
            prompt_drift=dto.prompt_drift,
            privacy_violation_count=dto.privacy_violation_count,
            evaluated_at=datetime.utcnow()
        )
        return self.repo.save(record)


class EvidenceLedgerService:
    def __init__(self, repo: EvidenceRepository):
        self.repo = repo
        
    def _hash_payload(self, payload: str) -> str:
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
    def record_evidence(self, asset_id: str, evidence_type: str, raw_payload: str, signer_id: str) -> EvidenceLedgerEntry:
        latest_record = self.repo.get_latest_by_asset(asset_id)
        prev_id = latest_record.id if latest_record else None
        
        # Link previous hash to new payload to create chain
        payload_hash = self._hash_payload(raw_payload)
        
        # Mocking PKI digital signature
        signature = f"sig_{self._hash_payload(payload_hash + signer_id)[:16]}"
        
        entry = EvidenceLedgerEntry(
            id=f"ledg_{uuid.uuid4().hex}",
            asset_id=asset_id,
            evidence_type=evidence_type,
            payload_hash=payload_hash,
            digital_signature=signature,
            signer_id=signer_id,
            previous_ledger_id=prev_id,
            recorded_at=datetime.utcnow()
        )
        return self.repo.save(entry)


class GovernanceWorkflowService:
    def __init__(self, repo: WorkflowRepository):
        self.repo = repo
        
    def transition_state(self, asset_id: str, workflow_type: str, new_state: str, comments: str = None) -> WorkflowState:
        # Very simplified state machine for demonstration
        state = WorkflowState(
            id=f"wf_{uuid.uuid4().hex}",
            asset_id=asset_id,
            workflow_type=workflow_type,
            current_state=new_state,
            comments=comments,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return self.repo.save(state)

class AssuranceService:
    """Orchestrates Continuous Assurance."""
    def __init__(self, trust_svc: TrustService, ledger_svc: EvidenceLedgerService):
        self.trust_svc = trust_svc
        self.ledger_svc = ledger_svc
        
    def verify_asset(self, asset_id: str) -> bool:
        trust = self.trust_svc.calculate_trust(asset_id)
        if trust.is_trusted:
            self.ledger_svc.record_evidence(
                asset_id, "CONTINUOUS_ASSURANCE", f"Asset {asset_id} passed assurance.", "system"
            )
            return True
        return False
