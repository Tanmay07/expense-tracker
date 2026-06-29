# Decision Learning Platform

The Enterprise Decision Learning, Memory & Adaptation Platform.

This package provides the core infrastructure for:
- **Decision Memory**: Storing decision history and context snapshots.
- **Pattern Mining**: Detecting behavioral and spending patterns.
- **Adaptive Personalization**: Adjusting recommendations based on user feedback.
- **Policy Decision Cache**: Replay-safe and version-aware decision caching.
- **Success Prediction**: Forecasting decision acceptance and ROI.
- **Financial DNA & Behavioral Evolution**: Evolving user profiles.
- **Continuous Learning & Replay**: Non-destructive weight adjustments and explainability.

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
