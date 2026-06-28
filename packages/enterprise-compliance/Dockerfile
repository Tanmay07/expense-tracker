FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install poetry or hatchling if needed, here we use pip with pyproject.toml
COPY pyproject.toml README.md ./
COPY enterprise_compliance/ ./enterprise_compliance/

# We just use pip to install the package and its dependencies
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "enterprise_compliance.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
