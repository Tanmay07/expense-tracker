# 001 - Adopt uv for Monorepo Workspace Management

**Date:** 2026-06-28
**Status:** Accepted

## Context
As the AI Personal Finance OS expands across multiple bounded contexts (Ledger, Agent Runtime, Core SDK, AI Platform), maintaining them in a single flat directory causes severe boundary leakage and dependency conflicts. We must transition to a package-by-domain monorepo strategy.

## Decision
We will adopt **uv** by Astral as our Python workspace manager.
1. `apps/` will contain deployable endpoints (e.g. FastAPI gateways).
2. `packages/` will contain strictly isolated domain logic.
3. `shared/` will contain foundational cross-cutting concerns (DTOs, Telemetry).

## Consequences
- **Positive:** Absolute domain isolation (Hexagonal Architecture). Millisecond resolution of package graphs.
- **Negative:** Slightly higher initial setup cost for developers to understand workspace boundaries. CI pipelines must become graph-aware to avoid running all tests on every commit.
