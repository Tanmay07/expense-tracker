from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from observability_platform.infrastructure.database import (
    TelemetryEventModel, MetricRecordModel, IncidentModel,
    SLORecordModel, DashboardConfigModel
)
from observability_platform.domain.models import (
    TelemetryEvent, MetricRecord, Incident,
    SLORecord, DashboardConfig
)

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

class TelemetryRepository(BaseRepository):
    def save(self, domain: TelemetryEvent) -> TelemetryEvent:
        model = self.session.execute(
            select(TelemetryEventModel).where(TelemetryEventModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = TelemetryEventModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return TelemetryEvent.model_validate(model)
        
    def get_by_category(self, category: str, limit: int = 100) -> List[TelemetryEvent]:
        results = self.session.execute(
            select(TelemetryEventModel)
            .where(TelemetryEventModel.category == category)
            .order_by(TelemetryEventModel.timestamp.desc())
            .limit(limit)
        ).scalars().all()
        return [TelemetryEvent.model_validate(r) for r in results]


class MetricRepository(BaseRepository):
    def save(self, domain: MetricRecord) -> MetricRecord:
        model = self.session.execute(
            select(MetricRecordModel).where(MetricRecordModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = MetricRecordModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return MetricRecord.model_validate(model)


class IncidentRepository(BaseRepository):
    def save(self, domain: Incident) -> Incident:
        model = self.session.execute(
            select(IncidentModel).where(IncidentModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = IncidentModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return Incident.model_validate(model)


class SLORepository(BaseRepository):
    def save(self, domain: SLORecord) -> SLORecord:
        model = self.session.execute(
            select(SLORecordModel).where(SLORecordModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = SLORecordModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return SLORecord.model_validate(model)


class DashboardRepository(BaseRepository):
    def save(self, domain: DashboardConfig) -> DashboardConfig:
        model = self.session.execute(
            select(DashboardConfigModel).where(DashboardConfigModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = DashboardConfigModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return DashboardConfig.model_validate(model)
