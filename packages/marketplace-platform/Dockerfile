FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy package metadata
COPY pyproject.toml README.md ./

# Install dependencies using pip
RUN pip install --no-cache-dir hatchling uv \
    && uv pip install --system -e .

# Copy application code
COPY . .

# Run the API server
CMD ["uvicorn", "marketplace_platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
