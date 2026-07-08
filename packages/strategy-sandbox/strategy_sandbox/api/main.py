from fastapi import FastAPI
from strategy_sandbox.api.routers import router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title="Strategy Sandbox Platform API",
    description="Enterprise Strategy Sandbox & Validation Platform",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1", tags=["sandbox"])


@app.on_event("startup")
def startup_event():
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "strategy-sandbox"}
