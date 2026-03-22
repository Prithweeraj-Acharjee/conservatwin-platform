"""
Museum management routes.
Register a museum, get dashboard data, manage zones.
"""

import secrets
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import get_db

router = APIRouter(prefix="/api/museums", tags=["museums"])


class MuseumCreate(BaseModel):
    name: str
    location: str | None = None
    slug: str


class ZoneCreate(BaseModel):
    name: str
    description: str | None = None
    target_temp_min: float = 18.0
    target_temp_max: float = 22.0
    target_rh_min: float = 40.0
    target_rh_max: float = 55.0
    material_type: str = "general"


@router.post("/register")
async def register_museum(data: MuseumCreate):
    api_key = f"ct_{secrets.token_urlsafe(32)}"
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO museums (name, slug, location, api_key) VALUES (?, ?, ?, ?)",
            (data.name, data.slug, data.location, api_key),
        )
        await db.commit()
    except Exception:
        await db.close()
        raise HTTPException(status_code=400, detail="Museum slug already exists")
    await db.close()
    return {
        "message": f"Museum '{data.name}' registered successfully",
        "api_key": api_key,
        "slug": data.slug,
        "important": "Save this API key — you'll need it for sensor configuration. It won't be shown again.",
    }


@router.get("/{slug}")
async def get_museum(slug: str):
    db = await get_db()
    row = await db.execute("SELECT id, name, slug, location, created_at, public FROM museums WHERE slug = ?", (slug,))
    museum = await row.fetchone()
    if not museum:
        await db.close()
        raise HTTPException(status_code=404, detail="Museum not found")

    museum = dict(museum)
    zones_rows = await db.execute("SELECT * FROM zones WHERE museum_id = ?", (museum["id"],))
    zones = [dict(z) for z in await zones_rows.fetchall()]
    await db.close()

    return {"museum": museum, "zones": zones}


@router.post("/{slug}/zones")
async def add_zone(slug: str, data: ZoneCreate):
    db = await get_db()
    row = await db.execute("SELECT id FROM museums WHERE slug = ?", (slug,))
    museum = await row.fetchone()
    if not museum:
        await db.close()
        raise HTTPException(status_code=404, detail="Museum not found")

    await db.execute(
        """INSERT INTO zones (museum_id, name, description, target_temp_min, target_temp_max,
           target_rh_min, target_rh_max, material_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (museum["id"], data.name, data.description, data.target_temp_min,
         data.target_temp_max, data.target_rh_min, data.target_rh_max, data.material_type),
    )
    await db.commit()
    await db.close()
    return {"message": f"Zone '{data.name}' added to museum"}


@router.get("")
async def list_public_museums():
    db = await get_db()
    rows = await db.execute("SELECT id, name, slug, location, created_at FROM museums WHERE public = 1")
    museums = [dict(r) for r in await rows.fetchall()]

    for museum in museums:
        zone_count = await db.execute("SELECT COUNT(*) as c FROM zones WHERE museum_id = ?", (museum["id"],))
        museum["zone_count"] = (await zone_count.fetchone())["c"]

        reading_count = await db.execute(
            """SELECT COUNT(*) as c FROM readings r
               JOIN zones z ON r.zone_id = z.id
               WHERE z.museum_id = ?""",
            (museum["id"],),
        )
        museum["total_readings"] = (await reading_count.fetchone())["c"]

    await db.close()
    return {"museums": museums}
