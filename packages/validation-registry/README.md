# Enterprise Validation Artifact Registry (VAR)

This package acts as the canonical repository for every validation artifact generated across the platform.

Key capabilities:
- **Centralized Registry**: Manages versioned validation reports, simulation outputs, and evidence packages.
- **Pluggable Storage Layer**: Supports local fallback with seamless scaling to AWS S3.
- **Graph Lineage**: Tracks relationships from Sandbox Runs to specific Artifacts.
- **Cryptographic Verification**: Secures artifacts with SHA-256 integrity checksums.
- **Evidence Bundling**: Generates unified evidence packages for compliance review.

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
