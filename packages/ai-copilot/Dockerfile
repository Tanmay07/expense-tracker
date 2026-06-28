FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY ai_copilot/ ./ai_copilot/
# Also copy ai-financial-coach as it is a local dependency
COPY ../ai-financial-coach/ ../ai-financial-coach/

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "ai_copilot.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
