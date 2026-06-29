from sqlalchemy.orm import Session
from typing import List, Optional

from .database import CapabilityModel, ApprovalRequestModel
from ..domain.models import ExecutionCapability, ApprovalRequest, ExecutionPrerequisite

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class CapabilityRepository(BaseRepository):
    def get_by_id(self, capability_id: str) -> Optional[ExecutionCapability]:
        record = self.db.query(CapabilityModel).filter(CapabilityModel.id == capability_id).first()
        if not record:
            return None
            
        prereqs = [ExecutionPrerequisite(**p) for p in record.prerequisites_json] if record.prerequisites_json else []
            
        return ExecutionCapability(
            id=record.id,
            name=record.name,
            description=record.description,
            automation_level=record.automation_level,
            risk_level=record.risk_level,
            supported_platforms=record.supported_platforms_json or [],
            prerequisites=prereqs,
            metadata=record.metadata_json or {},
            is_active=record.is_active,
            created_at=record.created_at
        )
        
    def list_all(self) -> List[ExecutionCapability]:
        records = self.db.query(CapabilityModel).all()
        result = []
        for r in records:
            prereqs = [ExecutionPrerequisite(**p) for p in r.prerequisites_json] if r.prerequisites_json else []
            result.append(ExecutionCapability(
                id=r.id,
                name=r.name,
                description=r.description,
                automation_level=r.automation_level,
                risk_level=r.risk_level,
                supported_platforms=r.supported_platforms_json or [],
                prerequisites=prereqs,
                metadata=r.metadata_json or {},
                is_active=r.is_active,
                created_at=r.created_at
            ))
        return result

    def save(self, capability: ExecutionCapability) -> ExecutionCapability:
        record = CapabilityModel(
            id=capability.id,
            name=capability.name,
            description=capability.description,
            automation_level=capability.automation_level.value,
            risk_level=capability.risk_level.value,
            supported_platforms_json=capability.supported_platforms,
            prerequisites_json=[p.model_dump() for p in capability.prerequisites],
            metadata_json=capability.metadata,
            is_active=capability.is_active,
            created_at=capability.created_at
        )
        self.db.merge(record)
        self.db.commit()
        return capability

class ApprovalRepository(BaseRepository):
    def save(self, request: ApprovalRequest) -> ApprovalRequest:
        record = ApprovalRequestModel(
            id=request.id,
            execution_step_id=request.execution_step_id,
            capability_id=request.capability_id,
            requested_by=request.requested_by,
            status=request.status.value,
            approver_id=request.approver_id,
            reason=request.reason,
            created_at=request.created_at,
            expires_at=request.expires_at
        )
        self.db.merge(record)
        self.db.commit()
        return request
