"""
Demo Seed Script
Populates the database with a sample museum and generates
realistic sensor data so anyone can see the platform in action.

Usage: python -m backend.demo_seed
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
        ("Gallery A - Impressionist Collection", "European oil paintings, 19th century", 19, 22, 45, 55, "oil_painting"),
        ("Gallery B - Asian Textiles", "Silk and cotton textiles, 15th-18th century", 18, 21, 45, 55, "textile"),
        ("Paper Conservation Vault", "Rare manuscripts and photographs", 16, 18, 40, 50, "paper"),
        ("Sculpture Hall", "Stone and ceramic works", 18, 24, 35, 55, "stone"),
    ]

    for name, desc, tmin, tmax, rhmin, rhmax, mat in zones:
        await db.execute(
            """INSERT OR IGNORE INTO zones (museum_id, name, description,
               target_temp_min, target_temp_max, target_rh_min, target_rh_max, material_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (museum_id, name, desc, tmin, tmax, rhmin, rhmax, mat),
        )

    rows = await db.execute("SELECT id, target_temp_min, target_temp_max, target_rh_min, target_rh_max FROM zones WHERE museum_id = ?", (museum_id,))
    zone_rows = [dict(z) for z in await rows.fetchall()]

    # Generate 24 hours of readings (one every 10 minutes = 144 readings per zone)
    now = datetime.now(timezone.utc)
    for zone in zone_rows:
        temp_mid = (zone["target_temp_min"] + zone["target_temp_max"]) / 2
        rh_mid = (zone["target_rh_min"] + zone["target_rh_max"]) / 2

        for i in range(144):
            ts = now - timedelta(minutes=(143 - i) * 10)
            hour = ts.hour + ts.minute / 60

            # Realistic diurnal pattern
            temp = temp_mid + 1.5 * math.sin((hour - 6) * math.pi / 12)
            rh = rh_mid - 3 * math.sin((hour - 6) * math.pi / 12)

            # Add some noise
            temp += random.gauss(0, 0.3)
            rh += random.gauss(0, 1.0)

            # Simulate an incident in zone 1 (humidity spike around hour 14)
            if zone == zone_rows[0] and 80 <= i <= 90:
                rh += 8 + random.gauss(0, 1)

            await db.execute(
                "INSERT INTO readings (zone_id, temperature, humidity, timestamp, source) VALUES (?, ?, ?, ?, ?)",
                (zone["id"], round(temp, 1), round(rh, 1), ts.isoformat(), "demo"),
            )

    await db.commit()
    await db.close()
    print("Demo data seeded successfully!")
    print("Museum: Toledo Museum of Art")
    print("Slug: toledo-museum")
    print("API Key: ct_demo_key_toledo_2024")
    print(f"Zones: {len(zones)}")
    print("Readings: 144 per zone (24 hours)")


if __name__ == "__main__":
    asyncio.run(seed())
