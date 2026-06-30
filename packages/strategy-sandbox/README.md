# Enterprise Strategy Sandbox & Validation Platform (SSVP)

This package provides the core infrastructure for the Strategy Sandbox Platform, acting as the mandatory pre-production CI/CD system for financial intelligence.

Key capabilities:
- **Validation Pipelines**: Multi-stage validation for strategies, templates, and AI prompts.
- **Historical Replay Validation**: Deterministic execution against point-in-time Digital Twin states.
- **Fitness Scoring Engine**: Composite scores for ROI, compliance, and risk.
- **AI Prompt Validation**: Hallucination resistance and policy compliance using LiteLLM.
- **Certification Platform**: Gatekeeping for the Enterprise Marketplace.

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
