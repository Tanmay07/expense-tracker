from fastapi import FastAPI
from platform_readiness.api.routers import router

# Import OpenTelemetry if available
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    HAS_OTEL = True
except ImportError:
    HAS_OTEL = False

app = FastAPI(
    title="Platform Readiness & Certification API",
    description="Enterprise Platform Readiness, Architecture Hardening & Production Certification Platform",
    version="1.0.0",
)

app.include_router(router)

if HAS_OTEL:
    FastAPIInstrumentor.instrument_app(app)
