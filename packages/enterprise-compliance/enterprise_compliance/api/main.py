from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .routers import router
from ..infrastructure.database import Base, engine

# Create tables if they don't exist (in a real app, use Alembic migrations instead)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Wealth Compliance & Suitability Platform",
    description="Wave 4C - Core policy evaluation engine for Personal Finance OS",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

FastAPIInstrumentor.instrument_app(app)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "enterprise-compliance"}
