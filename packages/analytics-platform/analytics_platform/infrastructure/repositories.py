from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from analytics_platform.infrastructure.database import (
    ExperimentRegistryModel,
    StatisticalGuardrailModel,
    KPICatalogModel,
    InsightModel,
    ExecutiveReportModel,
)
from analytics_platform.domain.models import (
    ExperimentRegistry,
    StatisticalGuardrail,
    KPICatalog,
    Insight,
    ExecutiveReport,
)


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session


class ExperimentRegistryRepository(BaseRepository):
    def save(self, domain: ExperimentRegistry) -> ExperimentRegistry:
        model = self.session.execute(
            select(ExperimentRegistryModel).where(
                ExperimentRegistryModel.id == domain.id
            )
        ).scalar_one_or_none()
        if not model:
            model = ExperimentRegistryModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ExperimentRegistry.model_validate(model)

    def get_by_name(self, name: str) -> Optional[ExperimentRegistry]:
        model = self.session.execute(
            select(ExperimentRegistryModel).where(ExperimentRegistryModel.name == name)
        ).scalar_one_or_none()
        return ExperimentRegistry.model_validate(model) if model else None


class StatisticalGuardrailRepository(BaseRepository):
    def save(self, domain: StatisticalGuardrail) -> StatisticalGuardrail:
        model = self.session.execute(
            select(StatisticalGuardrailModel).where(
                StatisticalGuardrailModel.id == domain.id
            )
        ).scalar_one_or_none()
        if not model:
            model = StatisticalGuardrailModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return StatisticalGuardrail.model_validate(model)

    def get_by_experiment_id(
        self, experiment_id: str
    ) -> Optional[StatisticalGuardrail]:
        model = self.session.execute(
            select(StatisticalGuardrailModel).where(
                StatisticalGuardrailModel.experiment_id == experiment_id
            )
        ).scalar_one_or_none()
        return StatisticalGuardrail.model_validate(model) if model else None


class KPICatalogRepository(BaseRepository):
    def save(self, domain: KPICatalog) -> KPICatalog:
        model = self.session.execute(
            select(KPICatalogModel).where(KPICatalogModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = KPICatalogModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return KPICatalog.model_validate(model)

    def get_by_name(self, name: str) -> Optional[KPICatalog]:
        model = self.session.execute(
            select(KPICatalogModel).where(KPICatalogModel.kpi_name == name)
        ).scalar_one_or_none()
        return KPICatalog.model_validate(model) if model else None


class InsightRepository(BaseRepository):
    def save(self, domain: Insight) -> Insight:
        model = self.session.execute(
            select(InsightModel).where(InsightModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = InsightModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return Insight.model_validate(model)


class ExecutiveReportRepository(BaseRepository):
    def save(self, domain: ExecutiveReport) -> ExecutiveReport:
        model = self.session.execute(
            select(ExecutiveReportModel).where(ExecutiveReportModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ExecutiveReportModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ExecutiveReport.model_validate(model)
