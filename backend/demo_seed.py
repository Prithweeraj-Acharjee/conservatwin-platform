"""
Demo Seed Script
Populates the database with a sample museum and generates
realistic 24-hour sensor data with museum-specific scenarios.
"""

import asyncio
import math
import random
from datetime import datetime, timedelta, timezone
from .database import init_db, get_db


async def seed():
    await init_db()
    db = await get_db()

    # Create demo museum
    await db.execute(
        "INSERT OR IGNORE INTO museums (name, slug, location, api_key, public) VALUES (?, ?, ?, ?, ?)",
        ("Toledo Museum of Art", "toledo-museum", "Toledo, Ohio, USA", "ct_demo_key_toledo_2024", 1),
    )

    row = await db.execute("SELECT id FROM museums WHERE slug = 'toledo-museum'")
    museum = await row.fetchone()
    museum_id = museum["id"]

    # Create zones with different material types
    zones = [
        ("Gallery A - Impressionist Collection", "European oil paintings, 19th century. Monet, Renoir, Degas.", 19, 22, 45, 55, "oil_painting"),
        ("Gallery B - Asian Textiles", "Silk and cotton textiles, 15th-18th century. Japanese kimonos and Chinese embroidery.", 18, 21, 45, 55, "textile"),
        ("Paper Conservation Vault", "Rare manuscripts, prints, and photographs. Climate-controlled archival storage.", 16, 18, 40, 50, "paper"),
        ("Sculpture Hall", "Greek and Roman marble, European bronze, contemporary ceramic.", 18, 24, 35, 55, "stone"),
    ]

    for name, desc, tmin, tmax, rhmin, rhmax, mat in zones:
        await db.execute(
            """INSERT OR IGNORE INTO zones (museum_id, name, description,
               target_temp_min, target_temp_max, target_rh_min, target_rh_max, material_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (museum_id, name, desc, tmin, tmax, rhmin, rhmax, mat),
        )

    rows = await db.execute(
        "SELECT id, name, target_temp_min, target_temp_max, target_rh_min, target_rh_max, material_type FROM zones WHERE museum_id = ?",
        (museum_id,),
    )
    zone_rows = [dict(z) for z in await rows.fetchall()]

    now = datetime.now(timezone.utc)
    random.seed(42)  # Reproducible data

    for zone in zone_rows:
        temp_mid = (zone["target_temp_min"] + zone["target_temp_max"]) / 2
        rh_mid = (zone["target_rh_min"] + zone["target_rh_max"]) / 2
        zone_idx = zone_rows.index(zone)

        # Generate 144 readings = one every 10 minutes for 24 hours
        for i in range(144):
            ts = now - timedelta(minutes=(143 - i) * 10)
            hour = ts.hour + ts.minute / 60

            # Base: realistic diurnal cycle (warmer in afternoon, cooler at night)
            temp = temp_mid + 1.2 * math.sin((hour - 6) * math.pi / 12)
            rh = rh_mid - 2.5 * math.sin((hour - 6) * math.pi / 12)

            # Small natural noise
            temp += random.gauss(0, 0.2)
            rh += random.gauss(0, 0.7)

            # === ZONE-SPECIFIC SCENARIOS ===

            # Gallery A (oil paintings): Humidity incident around 2-4 PM
            # Scenario: exterior door left open during humid afternoon
            if zone_idx == 0 and 84 <= i <= 96:
                severity = math.sin((i - 84) * math.pi / 12) * 12
                rh += severity
                temp += severity * 0.25

            # Gallery B (textiles): Stable but slightly warm in afternoon
            # Scenario: sunlight through windows raises temp
            if zone_idx == 1 and 72 <= i <= 108:
                temp += 0.8 * math.sin((i - 72) * math.pi / 36)

            # Paper vault: Very stable (well-controlled)
            # Scenario: brief HVAC hiccup at 3 AM
            if zone_idx == 2 and 30 <= i <= 36:
                temp += 1.5 * math.sin((i - 30) * math.pi / 6)
                rh -= 3 * math.sin((i - 30) * math.pi / 6)

            # Sculpture hall: Most tolerant, broad range
            # Scenario: visitor event in evening caused temp spike
            if zone_idx == 3 and 108 <= i <= 120:
                temp += 2.0 * math.sin((i - 108) * math.pi / 12)
                rh += 3.0 * math.sin((i - 108) * math.pi / 12)

            temp = round(temp, 1)
            rh = round(max(20, min(85, rh)), 1)

            await db.execute(
                "INSERT INTO readings (zone_id, temperature, humidity, timestamp, source) VALUES (?, ?, ?, ?, ?)",
                (zone["id"], temp, rh, ts.strftime("%Y-%m-%d %H:%M:%S"), "demo"),
            )

            # Store PRI for trend data (every 6th reading = every hour)
            if i % 6 == 0:
                from .engine.pri import calculate_pri
                recent_readings = [{"temperature": temp, "humidity": rh}]
                pri_result = calculate_pri(
                    recent_readings,
                    zone["target_temp_min"], zone["target_temp_max"],
                    zone["target_rh_min"], zone["target_rh_max"],
                    zone["material_type"],
                )
                await db.execute(
                    "INSERT INTO pri_history (zone_id, pri_value, temp_deviation, rh_deviation, stability_score, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (zone["id"], pri_result.pri, pri_result.temp_deviation, pri_result.rh_deviation, pri_result.stability_score, ts.strftime("%Y-%m-%d %H:%M:%S")),
                )

        # Generate alerts for Gallery A humidity incident
        if zone_idx == 0:
            alert_time = now - timedelta(minutes=50 * 10)
            await db.execute(
                "INSERT INTO alerts (zone_id, severity, message, pri_value, created_at) VALUES (?, ?, ?, ?, ?)",
                (zone["id"], "warning", "Humidity rising above target range. Currently 58.2% RH (target: 45-55%). Monitor for continued increase.", 35.0, alert_time.strftime("%Y-%m-%d %H:%M:%S")),
            )
            alert_time2 = now - timedelta(minutes=44 * 10)
            await db.execute(
                "INSERT INTO alerts (zone_id, severity, message, pri_value, created_at) VALUES (?, ?, ?, ?, ?)",
                (zone["id"], "critical", "Humidity critically high at 65.8% RH. Oil paintings at risk of canvas warping and paint delamination. Deploy dehumidifiers immediately.", 72.0, alert_time2.strftime("%Y-%m-%d %H:%M:%S")),
            )
            alert_time3 = now - timedelta(minutes=38 * 10)
            await db.execute(
                "INSERT INTO alerts (zone_id, severity, message, pri_value, created_at) VALUES (?, ?, ?, ?, ?)",
                (zone["id"], "info", "Humidity returning to normal range. Incident lasted approximately 2 hours. Recommend inspection of exterior door seals.", 18.0, alert_time3.strftime("%Y-%m-%d %H:%M:%S")),
            )

    await db.commit()
    await db.close()
    print("Demo data seeded successfully!")
    print("Museum: Toledo Museum of Art")
    print("Slug: toledo-museum")
    print("API Key: ct_demo_key_toledo_2024")
    print(f"Zones: {len(zones)}")
    print("Readings: 144 per zone (24 hours, every 10 min)")


if __name__ == "__main__":
    asyncio.run(seed())
