from fastapi import FastAPI
from validation_registry.api.routers import router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title="Validation Artifact Registry API",
    description="Enterprise Validation Artifact Registry (VAR)",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1", tags=["registry"])


@app.on_event("startup")
def startup_event():
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "validation-registry"}
