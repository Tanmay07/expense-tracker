# Personal Finance Operating System

Welcome to the **Personal Finance Operating System**, a comprehensive, multi-agent, enterprise-grade architecture for managing and optimizing personal financial data, decisions, and execution.

This repository (`finance-os-ledger`) implements the highly scalable backend of the OS, composed of multiple decoupled platforms leveraging Domain-Driven Design (DDD), Clean Architecture, and event-driven patterns.

## Architecture Modules

The OS is divided into several specialized packages inside the `packages/` directory:

1. **`core-ledger`**: The foundational double-entry ledger that acts as the single source of truth for all financial transactions, balances, and atomic movements.
2. **`financial-planning`**: Handles budgets, forecasts, goals, and strategic financial tracking over time.
3. **`data-intelligence`**: The ingestion and normalization engine. It transforms raw, unstructured data (receipts, PDFs, API payloads) into structured financial events using advanced LLM reasoning.
4. **`decision-registry`**: The canonical System of Record for every financial decision generated across the OS. It links decisions to user objectives.
5. **`decision-optimization`**: The intelligence engine that generates, ranks, and compares potential financial decisions.
6. **`decision-lifecycle`**: Manages the state machine and progression of decisions (from draft, to queued, to execution).
7. **`execution-capability`**: Determines *how* an action is performed, managing routing to plugins, human operators, or external APIs based on capabilities and risk levels.
8. **`execution-policy`**: The definitive authorization layer. It evaluates context snapshots against an AST-based rule engine to explicitly `ALLOW`, `DENY`, or `REQUIRE_APPROVAL` before execution.
9. **`integration-platform`**: The centralized nervous system (EFCIP) managing third-party connectors, normalization, rate-limiting, and webhook ingestion.
10. **`mission-control` & `mission-control-bff`**: The unified enterprise UI backend and command center providing an orchestrator view over finances.
11. **`collaboration-platform`**: The Enterprise Collaboration, Household & Advisor Platform (ECHAP). Handles multi-user governance, advisor roles, delegations, shared workspaces, and secure messaging.
## Technology Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** PostgreSQL (SQLAlchemy 2.0, Alembic)
- **Background Jobs:** Celery & Redis
- **Containerization:** Docker & Docker Compose
- **Observability:** OpenTelemetry ready

## Running Locally

To spin up the entire operating system, simply use `docker-compose`:

```bash
docker-compose up --build
```

This will launch PostgreSQL, Redis, and all FastAPI services and Celery workers for the various packages.

## Core Philosophy

- **No monolithic decision making**: The AI Copilot/Coach does not compute finances directly; it consumes platform SDKs.
- **Explainability**: Every decision, policy evaluation, and ledger entry must be entirely replayable, auditable, and traceable.
- **Separation of Concerns**: 
  - *Optimization Engine* decides WHAT to do.
  - *Lifecycle Platform* decides WHEN it happens.
  - *Execution Capability* decides HOW it happens.
  - *Execution Policy* decides WHETHER it is permitted.
