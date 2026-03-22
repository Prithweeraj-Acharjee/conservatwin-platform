"""
ConservaTwin Platform — Main Application
Open-source digital twin for cultural heritage preservation.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import museums, sensors, public


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="ConservaTwin Platform",
    description="Open-source digital twin for cultural heritage preservation. "
    "Monitor environmental conditions, calculate preservation risk, "
    "and receive AI-powered conservation recommendations.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(museums.router)
app.include_router(sensors.router)
app.include_router(public.router)


@app.get("/")
async def root():
    return {
        "name": "ConservaTwin Platform",
        "version": "0.1.0",
        "description": "Open-source digital twin for cultural heritage preservation",
        "docs": "/docs",
        "endpoints": {
            "register_museum": "POST /api/museums/register",
            "add_zone": "POST /api/museums/{slug}/zones",
            "send_reading": "POST /api/sensors/reading",
            "public_dashboard": "GET /api/public/{slug}",
            "list_museums": "GET /api/museums",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
