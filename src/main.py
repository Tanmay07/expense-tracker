from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api import router as accounts_router
from src.infrastructure.models import Base
from src.infrastructure.database import engine

# Create the tables (In production, use Alembic migrations instead)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance OS - Accounts & Ledger API",
    description="Core financial engine module for managing accounts and immutable ledger entries.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts_router, prefix="/api/v1", tags=["accounts"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "finance-os-ledger"}
