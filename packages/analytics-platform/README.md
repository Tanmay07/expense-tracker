# Enterprise Analytics, Experiment Intelligence & Continuous Improvement Platform (AECIP)

This package implements the Enterprise Intelligence Layer of the Personal Financial Operating System.

Key capabilities:
- **Statistical Guardrails**: Validates experiments with power analysis, MDE, and stopping rules.
- **KPI Catalog**: A centralized metadata registry for business, financial, and AI KPIs.
- **Insight Engine**: Discovers anomalies, regressions, and optimization opportunities.
- **Executive Reporting**: Generates scorecards and board-ready reports.

## Installation

This package is managed via `uv` at the monorepo root:

```bash
uv sync --all-packages
```

## Running Locally

To spin up the service (along with its Celery workers), use Docker Compose at the monorepo root:

```bash
docker-compose up --build
```
