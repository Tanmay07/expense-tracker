# PFOS Developer Guide

Welcome to the Personal Financial Operating System (PFOS) Platform. This guide explains how to use the Local Developer Platform for day-to-day engineering.

## 1. Prerequisites
- **Docker & Docker Compose**: Required for running services locally.
- **uv**: Python package and project manager.
- **make**: For executing standardized development workflows.
- **Flutter SDK**: For mobile client development.

## 2. Onboarding (One-Command Setup)
To bootstrap your local environment, simply run:
```bash
make setup
```
This will check dependencies, generate a `.env` file, create necessary state directories, and pull the required base images (PostgreSQL, Redis).

## 3. Standard Workflows

### Starting the Platform
You can start the entire platform or specific profiles using Docker Compose.

**Start all services:**
```bash
make start
```

**Start specific profiles:**
```bash
PROFILE=backend make start
PROFILE=frontend make start
```

### Stopping and Resetting
To gracefully stop all containers:
```bash
make stop
```

To completely wipe the environment (removes volumes, dropping databases):
```bash
make reset
```

### Testing and Quality
Run the unified test suite:
```bash
make test
```

Run static analysis, linting, and formatting:
```bash
make lint
make format
```

## 4. Docker Compose Profiles
The `docker-compose.yml` file is organized into functional profiles.
- `backend`: Runs all the core Python API services and Celery workers.
- `frontend`: Runs the Mission Control UI.
- `bff`: Runs the Backend-for-Frontend services.
- `db`: Runs PostgreSQL and Redis infrastructure.

## 5. IDE Support
We recommend using **VS Code** or **Cursor**. Ensure you configure your IDE to use the virtual environment managed by `uv` for Python type hinting.

For Flutter development, ensure the `client_extension_framework` and `mobile_sdk` paths are correctly resolved by running `flutter pub get` in those packages.
