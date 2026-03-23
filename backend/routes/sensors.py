"""
Sensor data ingestion routes.
ESP32 sensors POST readings here every 30 seconds.
Each reading triggers PRI calculation, anomaly detection, and alert generation.
"""

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from ..database import get_db
from ..engine.pri import calculate_pri
from ..engine.anomaly import detect_anomalies
from ..engine.advisor import generate_recommendations

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


class SensorReading(BaseModel):
    zone_id: int
    temperature: float
    humidity: float
    timestamp: str | None = None


class BatchReading(BaseModel):
    readings: list[SensorReading]


@router.post("/reading")
async def ingest_reading(data: SensorReading, x_api_key: str = Header(...)):
    db = await get_db()

    # Verify API key and zone ownership
    row = await db.execute(
        """SELECT z.*, m.api_key FROM zones z
           JOIN museums m ON z.museum_id = m.id
           WHERE z.id = ? AND m.api_key = ?""",
        (data.zone_id, x_api_key),
    )
    zone = await row.fetchone()
    if not zone:
        await db.close()
        raise HTTPException(status_code=403, detail="Invalid API key or zone not found")
    zone = dict(zone)

    # Store reading
    if data.timestamp:
        await db.execute(
            "INSERT INTO readings (zone_id, temperature, humidity, timestamp) VALUES (?, ?, ?, ?)",
            (data.zone_id, data.temperature, data.humidity, data.timestamp),
        )
    else:
        await db.execute(
            "INSERT INTO readings (zone_id, temperature, humidity) VALUES (?, ?, ?)",
            (data.zone_id, data.temperature, data.humidity),
        )

    # Get recent readings for analysis
    rows = await db.execute(
        "SELECT temperature, humidity, timestamp FROM readings WHERE zone_id = ? ORDER BY rowid DESC LIMIT 30",
        (data.zone_id,),
    )
    readings = [dict(r) for r in await rows.fetchall()]
    readings.reverse()

    # Calculate PRI
    pri_result = calculate_pri(
        readings, zone["target_temp_min"], zone["target_temp_max"],
        zone["target_rh_min"], zone["target_rh_max"], zone["material_type"],
    )

    # Store PRI
    await db.execute(
        "INSERT INTO pri_history (zone_id, pri_value, temp_deviation, rh_deviation, stability_score) VALUES (?, ?, ?, ?, ?)",
        (data.zone_id, pri_result.pri, pri_result.temp_deviation, pri_result.rh_deviation, pri_result.stability_score),
    )

    # Detect anomalies
    anomalies = detect_anomalies(
        readings, zone["target_temp_min"], zone["target_temp_max"],
        zone["target_rh_min"], zone["target_rh_max"],
    )

    # Generate alerts for anomalies and high PRI
    for anomaly in anomalies:
        await db.execute(
            "INSERT INTO alerts (zone_id, severity, message, pri_value) VALUES (?, ?, ?, ?)",
            (data.zone_id, anomaly.severity, anomaly.message, pri_result.pri),
        )

    if pri_result.pri >= 70 and pri_result.risk_level == "critical":
        await db.execute(
            "INSERT INTO alerts (zone_id, severity, message, pri_value) VALUES (?, ?, ?, ?)",
            (data.zone_id, "critical", f"PRI is critical ({pri_result.pri}). {'; '.join(pri_result.factors)}", pri_result.pri),
        )
    elif pri_result.pri >= 45 and pri_result.risk_level == "high":
        await db.execute(
            "INSERT INTO alerts (zone_id, severity, message, pri_value) VALUES (?, ?, ?, ?)",
            (data.zone_id, "warning", f"PRI is elevated ({pri_result.pri}). {'; '.join(pri_result.factors)}", pri_result.pri),
        )

    await db.commit()
    await db.close()

    return {
        "status": "ok",
        "pri": {
            "value": pri_result.pri,
            "risk_level": pri_result.risk_level,
            "factors": pri_result.factors,
        },
        "anomalies": [{"type": a.anomaly_type, "severity": a.severity, "message": a.message} for a in anomalies],
    }


@router.post("/batch")
async def ingest_batch(data: BatchReading, x_api_key: str = Header(...)):
    results = []
    for reading in data.readings:
        result = await ingest_reading(reading, x_api_key)
        results.append(result)
    return {"results": results}
