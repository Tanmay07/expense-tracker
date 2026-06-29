from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .routers import router
from ..infrastructure.database import Base, engine

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Decision Registry Platform",
    description="Phase 10B.1 - System of Record for all Financial Decisions",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1/decision-registry")

FastAPIInstrumentor.instrument_app(app)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "decision-registry"}
