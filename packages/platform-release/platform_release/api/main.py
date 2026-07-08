from fastapi import FastAPI
from platform_release.api.routers import router, engine
from platform_release.infrastructure.database.models import Base

# Initialize DB (in memory for now)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Platform Release API", version="1.0.0")

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
