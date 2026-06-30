import uuid
import numpy as np
import polars as pl
from scipy import stats
from datetime import datetime
from typing import Optional, List, Dict, Any

from analytics_platform.domain.models import (
    ExperimentRegistry, ExperimentRegistryCreate,
    StatisticalGuardrail, KPICatalog, Insight, ExecutiveReport
)
from analytics_platform.infrastructure.repositories import (
    ExperimentRegistryRepository, StatisticalGuardrailRepository,
    KPICatalogRepository, InsightRepository, ExecutiveReportRepository
)

class StatisticalGuardrailService:
    def __init__(self, repo: StatisticalGuardrailRepository):
        self.repo = repo
        
    def calculate_mde(self, baseline_conversion: float, sample_size: int, alpha: float = 0.05, power: float = 0.8) -> float:
        """
        Mock Minimum Detectable Effect calculation using statistical power.
        """
        # In a real impl, we'd use statsmodels.stats.power.zt_ind_solve_power
        # For MVP, return a mock calculated effect size based on the inputs
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        # Simplified standard error assumption
        p = baseline_conversion
        se = np.sqrt(2 * p * (1-p) / (sample_size/2))
        mde = (z_alpha + z_beta) * se
        return float(mde)

    def validate_guardrails(self, experiment_id: str) -> bool:
        guardrail = self.repo.get_by_experiment_id(experiment_id)
        if not guardrail:
            return False
        # Ensures sample size meets minimum thresholds
        return guardrail.min_sample_size > 0

class ExperimentRegistryService:
    def __init__(self, repo: ExperimentRegistryRepository, guardrail_svc: StatisticalGuardrailService):
        self.repo = repo
        self.guardrail_svc = guardrail_svc
        
    def register_experiment(self, dto: ExperimentRegistryCreate) -> ExperimentRegistry:
        exp = ExperimentRegistry(
            id=f"exp_reg_{uuid.uuid4().hex}",
            name=dto.name,
            description=dto.description,
            owner_id=dto.owner_id,
            business_objective=dto.business_objective,
            hypothesis=dto.hypothesis,
            feature_id=dto.feature_id,
            status="REGISTERED",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return self.repo.save(exp)
        
    def get_experiment(self, name: str) -> Optional[ExperimentRegistry]:
        return self.repo.get_by_name(name)

class KPICatalogService:
    def __init__(self, repo: KPICatalogRepository):
        self.repo = repo
        
    def register_kpi(self, domain: KPICatalog) -> KPICatalog:
        return self.repo.save(domain)

    def get_kpi(self, name: str) -> Optional[KPICatalog]:
        return self.repo.get_by_name(name)

class ExperimentAnalyticsService:
    def analyze_results(self, experiment_id: str, results_df: pl.DataFrame) -> Dict[str, Any]:
        """
        Utilizes polars and scipy to calculate significance.
        """
        # Mock analysis
        return {
            "lift": 0.05,
            "p_value": 0.03,
            "significant": True
        }

class BusinessAnalyticsService:
    pass

class AIAnalyticsService:
    pass

class ContinuousImprovementService:
    def detect_drift(self, kpi_history: List[float]) -> bool:
        """
        Returns true if the recent mean diverges significantly.
        """
        if len(kpi_history) < 10:
            return False
        recent = kpi_history[-5:]
        older = kpi_history[:-5]
        # Welch's t-test
        stat, p = stats.ttest_ind(recent, older, equal_var=False)
        return float(p) < 0.05

class InsightEngineService:
    def __init__(self, repo: InsightRepository):
        self.repo = repo
        
    def generate_insight(self, title: str, description: str, severity: str = "INFO") -> Insight:
        ins = Insight(
            id=f"ins_{uuid.uuid4().hex}",
            insight_type="ANOMALY",
            severity=severity,
            title=title,
            description=description,
            generated_at=datetime.utcnow()
        )
        return self.repo.save(ins)

class ExecutiveReportingService:
    def __init__(self, repo: ExecutiveReportRepository):
        self.repo = repo
        
    def generate_weekly_report(self) -> ExecutiveReport:
        rep = ExecutiveReport(
            id=f"rep_{uuid.uuid4().hex}",
            report_type="WEEKLY",
            content_json={"overall_health": "good", "kpis_met": 15},
            generated_at=datetime.utcnow()
        )
        return self.repo.save(rep)
