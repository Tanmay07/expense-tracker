from fastapi import FastAPI
from hierarchical_learning.api.routers import router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title="Hierarchical Learning Platform API",
    description="Enterprise Hierarchical Learning & Knowledge Evolution Platform for PFOS",
    version="0.1.0",
)

app.include_router(router, prefix="/learning", tags=["learning"])

@app.on_event("startup")
def startup_event():
    # Attempt OpenTelemetry instrumentation. In a real environment, the provider would be configured.
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass
        
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "hierarchical-learning"}
