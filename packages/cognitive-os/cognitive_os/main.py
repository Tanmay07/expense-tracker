from fastapi import FastAPI
from .api.routes import router as cognition_router

app = FastAPI(
    title="Enterprise Cognitive Financial Operating System (CFOS)",
    description="The continuous intelligence engine of PFOS",
    version="0.1.0",
)

app.include_router(cognition_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "cognitive-os"}
