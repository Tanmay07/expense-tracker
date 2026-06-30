# Enterprise Decision Marketplace & Strategy Exchange

This package provides the core infrastructure for the Marketplace Platform, establishing the canonical distribution and governance layer for all financial knowledge, strategies, templates, and reusable decision assets.

Key capabilities:
- **Decision & Strategy Marketplace**: Publishing and discovery of reusable financial assets.
- **Knowledge Capability Matrix**: Governance contract for artifacts (scope, visibility, sensitivity, AI usability).
- **Trust & Certification**: Digital signatures, validation workflows.
- **Marketplace Ranking**: Scoring based on ROI, completion rate, freshness.
- **Marketplace Governance**: Lifecycle management (draft, publish, deprecate).

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
