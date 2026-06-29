FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
# We also need the local decision-registry for the dependency
COPY ../decision-registry /decision-registry
COPY decision_intelligence/ ./decision_intelligence/

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "decision_intelligence.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
