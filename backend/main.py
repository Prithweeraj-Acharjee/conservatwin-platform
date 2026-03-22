"""
ConservaTwin Platform — Main Application
Open-source digital twin for cultural heritage preservation.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, get_db
from .routes import museums, sensors, public


async def _auto_seed_if_empty():
    """Auto-seed demo data if database is empty (handles Render free tier /tmp wipes)."""
    try:
        db = await get_db()
        row = await db.execute("SELECT COUNT(*) as c FROM museums")
        count = (await row.fetchone())["c"]
        await db.close()
        if count == 0:
            print("[ConservaTwin] Database is empty, seeding demo data...")
            from .demo_seed import seed
            await seed()
            print("[ConservaTwin] Demo data seeded successfully!")
        else:
            print(f"[ConservaTwin] Database has {count} museum(s), skipping seed.")
    except Exception as e:
        print(f"[ConservaTwin] Auto-seed error: {e}")
        import traceback
        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await _auto_seed_if_empty()
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


@app.post("/seed")
async def manual_seed():
    """Manual seed endpoint — use if auto-seed fails."""
    from .demo_seed import seed
    await seed()
    return {"status": "seeded"}
