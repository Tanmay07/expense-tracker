# Enterprise Platform Readiness, Architecture Hardening & Production Certification Platform (PRAPC)

This package serves as the final quality gate in the PFOS ecosystem, ensuring every component meets enterprise production standards before going live.

Key capabilities:
- **Architecture Fitness**: Validates CQRS boundaries, layer separation, and cyclic dependencies.
- **Security & Performance Certification**: Threat modeling, vulnerability scanning, and load testing orchestration.
- **Chaos Engineering**: Simulates infrastructure failure (e.g., Redis down, DB down) to evaluate graceful degradation.
- **Production Readiness Score**: Aggregates all certifications into an objective Go/No-Go index.

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
