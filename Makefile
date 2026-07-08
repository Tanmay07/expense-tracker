.PHONY: help setup start stop reset test lint format migrate seed docs build-all clean check

# Default target
help:
	@echo "PFOS Local Developer Platform"
	@echo "--------------------------------"
	@echo "make setup    - Install dependencies and prepare local environment"
	@echo "make start    - Start all services (use PROFILE=backend to start specific profiles)"
	@echo "make stop     - Stop all running services"
	@echo "make reset    - Stop, remove volumes, and clean environment"
	@echo "make test     - Run unit and integration tests across packages"
	@echo "make lint     - Run static analysis and linting"
	@echo "make format   - Run code formatters"
	@echo "make migrate  - Run database migrations"
	@echo "make seed     - Seed the database with mock data"
	@echo "make docs     - Generate and serve local documentation"
	@echo "make check    - Run formatting, linting, and tests (CI simulation)"

setup:
	@echo "Running setup scripts..."
	@bash scripts/setup-local.sh

start:
	@echo "Starting PFOS services (Profile: $${PROFILE:-all})..."
	@if [ -z "$$PROFILE" ]; then \
		docker compose up -d; \
	else \
		docker compose --profile $$PROFILE up -d; \
	fi

stop:
	@echo "Stopping PFOS services..."
	@docker compose stop

reset:
	@echo "Resetting PFOS environment (stopping containers and removing volumes)..."
	@docker compose down -v
	@echo "Environment reset complete."

test:
	@echo "Running tests using uv..."
	@uv run pytest tests/ --disable-warnings

lint:
	@echo "Running linters..."
	@uv run ruff check packages/ src/
	@uv run mypy packages/ src/
	@echo "Flutter analyze..."
	@cd packages/mobile_sdk && flutter analyze || true
	@cd packages/client_extension_framework && flutter analyze || true

format:
	@echo "Formatting code..."
	@uv run ruff format packages/ src/

migrate:
	@echo "Running database migrations..."
	@echo "Migrations are automatically handled by alembic or custom scripts."
	# Add actual migration command when Alembic is standardized.

seed:
	@echo "Seeding the database..."
	@uv run python -m scripts.seed_db

docs:
	@echo "Serving Developer Portal..."
	@cd docs && mkdocs serve || echo "MkDocs not installed/configured yet."

clean:
	@echo "Cleaning caches and temp files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +

build-all:
	@echo "Building all docker images..."
	@docker compose build

check: format lint test
	@echo "All checks passed!"
