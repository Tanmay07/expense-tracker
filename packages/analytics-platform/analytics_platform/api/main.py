from fastapi import FastAPI
from analytics_platform.api.routers import router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title="Enterprise Analytics Platform API",
    description="Experiment Intelligence & Continuous Improvement Platform",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1", tags=["analytics"])

@app.on_event("startup")
def startup_event():
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "analytics-platform"}
