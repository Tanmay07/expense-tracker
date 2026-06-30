# Hierarchical Learning Platform

The Enterprise Hierarchical Learning & Knowledge Evolution Platform (HLKEP).

This package provides the core infrastructure for:
- **Global Intelligence**: Aggregate anonymous learning across the platform.
- **Regional Intelligence**: Localized learning by country or jurisdiction.
- **Household Intelligence**: Shared habits, goals, and consensus models.
- **Personal Intelligence**: Financial DNA and behavioral outcomes.
- **Knowledge Promotion**: Governing the lifecycle of learned knowledge.
- **Privacy Boundary Engine**: Enforcing consent, data residency, and opt-outs.
- **Confidence & Decay Engines**: Managing knowledge relevance over time.

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
