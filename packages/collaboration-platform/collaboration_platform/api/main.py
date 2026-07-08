from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

from collaboration_platform.api.routers import router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Collaboration Platform API",
        description="Enterprise Collaboration, Household & Advisor Platform for PFOS",
        version="0.1.0",
    )

    app.include_router(router)

    # Instrument FastAPI with OpenTelemetry for observability
    FastAPIInstrumentor.instrument_app(app)

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "service": "collaboration-platform"}

    return app


app = create_app()
