FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY execution_policy/ ./execution_policy/

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "execution_policy.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
