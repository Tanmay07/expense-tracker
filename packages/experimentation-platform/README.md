# Enterprise Feature Flag, Experimentation & Progressive Delivery Platform (FFEP)

This package implements the canonical change management and progressive delivery engine for the Personal Financial Operating System.

Key capabilities:
- **Universal Feature Registry**: Registers models, prompts, policies, and UI elements.
- **Dynamic Feature Flags**: Metadata-driven rules engine.
- **Progressive Delivery**: Orchestrates Alpha/Beta/Canary/Global rollouts.
- **Experimentation Engine**: AI prompt comparisons and financial strategy A/B tests using MurmurHash3 for deterministic assignment.

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
