"""
Simple API key authentication for museums.
Each museum gets a unique API key when registered.
Sensors include this key in their POST requests.
"""

from fastapi import Header, HTTPException
from ..database import get_db


async def get_museum_by_api_key(x_api_key: str = Header(...)):
    db = await get_db()
    row = await db.execute("SELECT * FROM museums WHERE api_key = ?", (x_api_key,))
    museum = await row.fetchone()
    await db.close()
    if not museum:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return dict(museum)
