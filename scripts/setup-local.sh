#!/usr/bin/env bash
# PFOS Local Developer Environment Setup Script

set -e

echo "=============================================="
echo "    PFOS Developer Onboarding Setup"
echo "=============================================="

# 1. Check prerequisites
echo "[1/4] Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker is required but not installed. Aborting." >&2; exit 1; }
command -v uv >/dev/null 2>&1 || { echo "WARNING: uv is recommended but not installed." >&2; }
command -v make >/dev/null 2>&1 || { echo "ERROR: make is required but not installed. Aborting." >&2; exit 1; }

# 2. Setup environment variables
echo "[2/4] Setting up environment variables..."
if [ ! -f ".env" ]; then
    echo "Creating default .env file..."
    cat <<EOF > .env
# PFOS Local Environment Variables
ENVIRONMENT=development
POSTGRES_USER=ledger_user
POSTGRES_PASSWORD=ledger_password
POSTGRES_DB=finance_ledger
OPENAI_API_KEY=mock
EOF
    echo ".env created successfully."
else
    echo ".env already exists. Skipping."
fi

# 3. Create necessary local directories
echo "[3/4] Creating local state directories..."
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p data/artifacts

# 4. Pull required docker images
echo "[4/4] Pre-pulling infrastructure docker images..."
docker pull postgres:15
docker pull redis:7

echo "=============================================="
echo "    Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Run 'make start' to launch the core infrastructure."
echo "2. Run 'make test' to run the test suite."
echo "3. Consult docs/developer-guide.md for more info."
echo ""
