"""
Public dashboard routes.
Anyone can view a museum's heritage health profile.
No API key needed — this is the public-facing page.
"""

from fastapi import APIRouter, HTTPException
from ..database import get_db
from ..engine.pri import calculate_pri
from ..engine.advisor import generate_recommendations

router = APIRouter(prefix="/api/public", tags=["public"])


@router.get("/{slug}")
async def public_dashboard(slug: str):
    db = await get_db()

    row = await db.execute(
        "SELECT id, name, slug, location, created_at FROM museums WHERE slug = ? AND public = 1",
        (slug,),
    )
    museum = await row.fetchone()
    if not museum:
        await db.close()
        raise HTTPException(status_code=404, detail="Museum not found or not public")
    museum = dict(museum)

    zones_rows = await db.execute("SELECT * FROM zones WHERE museum_id = ?", (museum["id"],))
    zones = [dict(z) for z in await zones_rows.fetchall()]

    zone_data = []
    for zone in zones:
        # Latest readings
        rows = await db.execute(
            "SELECT temperature, humidity, timestamp FROM readings WHERE zone_id = ? ORDER BY rowid DESC LIMIT 30",
            (zone["id"],),
        )
        readings = [dict(r) for r in await rows.fetchall()]
        readings.reverse()

        # Calculate current PRI
        pri_result = calculate_pri(
            readings, zone["target_temp_min"], zone["target_temp_max"],
            zone["target_rh_min"], zone["target_rh_max"], zone["material_type"],
        )

        # Get recommendations
        current_temp = readings[-1]["temperature"] if readings else 0
        current_rh = readings[-1]["humidity"] if readings else 0

        recs = generate_recommendations(
            pri_result, current_temp, current_rh,
            zone["target_temp_min"], zone["target_temp_max"],
            zone["target_rh_min"], zone["target_rh_max"],
            zone["material_type"], len(readings),
        )

        # Recent alerts
        alert_rows = await db.execute(
            "SELECT severity, message, created_at FROM alerts WHERE zone_id = ? ORDER BY created_at DESC LIMIT 5",
            (zone["id"],),
        )
        alerts = [dict(a) for a in await alert_rows.fetchall()]

        # PRI trend (last 24 entries)
        pri_rows = await db.execute(
            "SELECT pri_value, timestamp FROM pri_history WHERE zone_id = ? ORDER BY timestamp DESC LIMIT 24",
            (zone["id"],),
        )
        pri_trend = [dict(p) for p in await pri_rows.fetchall()]
        pri_trend.reverse()

        zone_data.append({
            "zone": {
                "id": zone["id"],
                "name": zone["name"],
                "description": zone["description"],
                "material_type": zone["material_type"],
                "targets": {
                    "temp": [zone["target_temp_min"], zone["target_temp_max"]],
                    "rh": [zone["target_rh_min"], zone["target_rh_max"]],
                },
            },
            "current": {
                "temperature": current_temp,
                "humidity": current_rh,
                "timestamp": readings[-1]["timestamp"] if readings else None,
            },
            "pri": {
                "value": pri_result.pri,
                "risk_level": pri_result.risk_level,
                "factors": pri_result.factors,
                "trend": pri_trend,
            },
            "recommendations": [
                {"priority": r.priority, "action": r.action, "reason": r.reason, "category": r.category}
                for r in recs
            ],
            "recent_alerts": alerts,
            "readings_24h": readings,
        })

    await db.close()

    return {
        "museum": museum,
        "zones": zone_data,
        "overall_health": _calculate_overall_health(zone_data),
    }


def _calculate_overall_health(zone_data: list) -> dict:
    if not zone_data:
        return {"score": 100, "status": "no data"}

    pri_values = [z["pri"]["value"] for z in zone_data]
    avg_pri = sum(pri_values) / len(pri_values)
    worst_pri = max(pri_values)

    if worst_pri < 20:
        status = "excellent"
    elif worst_pri < 45:
        status = "good"
    elif worst_pri < 70:
        status = "needs attention"
    else:
        status = "critical"

    return {
        "average_pri": round(avg_pri, 1),
        "worst_pri": round(worst_pri, 1),
        "status": status,
        "zones_at_risk": sum(1 for p in pri_values if p >= 45),
    }
