from fastapi import FastAPI
from .routers import router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title="Decision Learning API",
    description="Enterprise Decision Learning, Memory & Adaptation Platform",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1/learning", tags=["Learning Platform"])

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "decision-learning"}
