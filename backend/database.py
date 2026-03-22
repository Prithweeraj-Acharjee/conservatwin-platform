"""
ConservaTwin Platform — Database Layer
Multi-tenant SQLite database for museums, zones, sensor readings, and alerts.
"""

import aiosqlite
import os
from datetime import datetime, timezone

DB_PATH = os.getenv("CT_DB_PATH", "conservatwin.db")


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def init_db():
    db = await get_db()
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS museums (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            slug        TEXT UNIQUE NOT NULL,
            location    TEXT,
            api_key     TEXT UNIQUE NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            public      INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS zones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            museum_id   INTEGER NOT NULL REFERENCES museums(id) ON DELETE CASCADE,
            name        TEXT NOT NULL,
            description TEXT,
            target_temp_min REAL DEFAULT 18.0,
            target_temp_max REAL DEFAULT 22.0,
            target_rh_min   REAL DEFAULT 40.0,
            target_rh_max   REAL DEFAULT 55.0,
            material_type   TEXT DEFAULT 'general',
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS readings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id     INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
            temperature REAL NOT NULL,
            humidity    REAL NOT NULL,
            timestamp   TEXT DEFAULT (datetime('now')),
            source      TEXT DEFAULT 'sensor'
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id     INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
            severity    TEXT NOT NULL CHECK(severity IN ('info','warning','critical')),
            message     TEXT NOT NULL,
            pri_value   REAL,
            acknowledged INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now')),
            resolved_at TEXT
        );

        CREATE TABLE IF NOT EXISTS pri_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id     INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
            pri_value   REAL NOT NULL,
            temp_deviation  REAL,
            rh_deviation    REAL,
            stability_score REAL,
            timestamp   TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_readings_zone_time ON readings(zone_id, timestamp);
        CREATE INDEX IF NOT EXISTS idx_alerts_zone ON alerts(zone_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_pri_zone_time ON pri_history(zone_id, timestamp);
    """)
    await db.commit()
    await db.close()
