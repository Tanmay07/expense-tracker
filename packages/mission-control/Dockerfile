FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY mission_control/ ./mission_control/

# Also copy SDKs if needed (mocked for now)
COPY ../ai-copilot/ ../ai-copilot/
COPY ../ai-financial-coach/ ../ai-financial-coach/

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "mission_control.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
