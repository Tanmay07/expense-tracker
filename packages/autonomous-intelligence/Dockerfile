FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir hatch hatchling uv

COPY pyproject.toml README.md ./
COPY autonomous_intelligence /app/autonomous_intelligence
COPY alembic /app/alembic
COPY alembic.ini /app/

RUN uv pip install --system -e .

CMD ["uvicorn", "autonomous_intelligence.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"]
