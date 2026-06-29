from sqlalchemy.orm import Session
from typing import List, Optional

from .database import DecisionModel, DecisionRelationshipModel
from ..domain.models import Decision, DecisionPriority, DecisionVersion, DecisionMetadata, DecisionProvenance, DecisionRelationship

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class DecisionRepository(BaseRepository):
    def get_by_id(self, decision_id: str) -> Optional[Decision]:
        record = self.db.query(DecisionModel).filter(DecisionModel.id == decision_id).first()
        if not record:
            return None
            
        priority = DecisionPriority(
            level=record.priority_level,
            importance_score=record.importance_score
        )
        
        version_info = DecisionVersion(
            version=record.version,
            semantic_version=record.semantic_version,
            created_at=record.created_at,
            rollback_metadata=record.rollback_metadata
        )
        
        metadata = DecisionMetadata(**record.metadata_json)
        provenance = DecisionProvenance(**record.provenance_json)
        
        return Decision(
            id=record.id,
            user_id=record.user_id,
            type=record.type,
            category=record.category,
            status=record.status,
            scope=record.scope,
            priority=priority,
            version_info=version_info,
            metadata=metadata,
            provenance=provenance,
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    def save(self, decision: Decision) -> Decision:
        record = DecisionModel(
            id=decision.id,
            user_id=decision.user_id,
            type=decision.type.value,
            category=decision.category.value,
            status=decision.status.value,
            scope=decision.scope.value,
            priority_level=decision.priority.level,
            importance_score=decision.priority.importance_score,
            version=decision.version_info.version,
            semantic_version=decision.version_info.semantic_version,
            rollback_metadata=decision.version_info.rollback_metadata,
            metadata_json=decision.metadata.model_dump(),
            provenance_json=decision.provenance.model_dump(),
            created_at=decision.created_at,
            updated_at=decision.updated_at
        )
        self.db.merge(record)
        self.db.commit()
        return decision

class DecisionRelationshipRepository(BaseRepository):
    def get_by_decision(self, decision_id: str) -> List[DecisionRelationship]:
        records = self.db.query(DecisionRelationshipModel).filter(
            DecisionRelationshipModel.source_decision_id == decision_id
        ).all()
        
        return [
            DecisionRelationship(
                id=r.id,
                source_decision_id=r.source_decision_id,
                target_id=r.target_id,
                target_type=r.target_type,
                relationship_type=r.relationship_type,
                metadata=r.metadata_json
            ) for r in records
        ]

    def save(self, rel: DecisionRelationship) -> DecisionRelationship:
        record = DecisionRelationshipModel(
            id=rel.id,
            source_decision_id=rel.source_decision_id,
            target_id=rel.target_id,
            target_type=rel.target_type,
            relationship_type=rel.relationship_type.value,
            metadata_json=rel.metadata
        )
        self.db.merge(record)
        self.db.commit()
        return rel
