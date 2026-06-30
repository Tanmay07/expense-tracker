from fastapi import FastAPI
from marketplace_platform.api.routers import router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title="Marketplace Platform API",
    description="Enterprise Decision Marketplace, Strategy Exchange & Knowledge Governance Platform",
    version="0.1.0",
)

app.include_router(router, prefix="/marketplace", tags=["marketplace"])

@app.on_event("startup")
def startup_event():
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass
        
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "marketplace-platform"}
