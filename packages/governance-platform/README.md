# Enterprise Governance, Trust & Assurance Platform (GTAP)

This package implements the canonical governance and trust layer of the Personal Financial Operating System.

Key capabilities:
- **Declarative Governance-as-Code**: Policies can be defined via API payloads and versioned.
- **Dynamic Trust Score**: Computes real-time trust metrics based on validation success, hallucination metrics, and AI compliance.
- **Evidence Ledger**: Append-only cryptographic ledger of governance approvals and verifications.
- **Workflow State Machine**: Tracks assets through Draft -> Review -> Approve maturity cycles.

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
