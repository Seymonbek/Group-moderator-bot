"""
Baza ulanish boshqaruvi (connection pool).
Singleton pattern — butun bot uchun bitta ulanish.
"""
import logging
import os

import aiosqlite

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "bot.db")

_db: aiosqlite.Connection | None = None


async def get_db() -> aiosqlite.Connection:
    """Mavjud baza ulanishini qaytaradi yoki yangi ulanish ochadi."""
    global _db
    if _db is None:
        _db = await aiosqlite.connect(DB_PATH)
        _db.row_factory = aiosqlite.Row
        await _db.execute("PRAGMA journal_mode=WAL")
        await _db.execute("PRAGMA foreign_keys=ON")
    return _db


async def close_db():
    """Baza ulanishini yopadi."""
    global _db
    if _db is not None:
        await _db.close()
        _db = None
        logger.info("Baza ulanishi yopildi.")
