from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import router

app = FastAPI(
    title="Mission Control BFF",
    version="1.0.0",
    description="Backend for Frontend for Mission Control OS"
)

# In a real enterprise app, CORS origins should be strict.
# For local development with Vite on port 3000:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "mission-control-bff"}
