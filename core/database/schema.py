"""
Baza sxemasi — barcha jadvallar shu yerda e'lon qilinadi.
Bot ishga tushganda init_db() chaqiriladi.
"""
import logging

from core.database.connection import get_db

logger = logging.getLogger(__name__)


async def init_db():
    """
    Bazani ishga tushiradi va barcha jadvallarni yaratadi.
    Bot ishga tushganda bir marta chaqiriladi.
    """
    db = await get_db()

    # ===== GURUH SOZLAMALARI =====
    await db.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            chat_id INTEGER PRIMARY KEY,
            anti_link INTEGER DEFAULT 0,
            anti_flood INTEGER DEFAULT 0,
            anti_bot INTEGER DEFAULT 0,
            anti_forward INTEGER DEFAULT 0,
            anti_arabic INTEGER DEFAULT 0,
            anti_emoji_spam INTEGER DEFAULT 0,
            bad_words_enabled INTEGER DEFAULT 0,
            captcha_enabled INTEGER DEFAULT 0,
            auto_delete_joins INTEGER DEFAULT 0,
            welcome_text TEXT DEFAULT NULL,
            log_channel_id INTEGER DEFAULT NULL,
            language TEXT DEFAULT 'uz',
            max_warns INTEGER DEFAULT 3,
            flood_limit INTEGER DEFAULT 5,
            flood_time INTEGER DEFAULT 10
        )
    """)

    # ===== OGOHLANTIRSHLAR =====
    await db.execute("""
        CREATE TABLE IF NOT EXISTS warns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            reason TEXT,
            admin_id INTEGER,
            admin_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ===== MODERATSIYA TARIXI =====
    await db.execute("""
        CREATE TABLE IF NOT EXISTS actions_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            user_id INTEGER,
            user_name TEXT,
            admin_id INTEGER,
            admin_name TEXT,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ===== XABAR STATISTIKASI =====
    await db.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            message_date DATE NOT NULL,
            msg_count INTEGER DEFAULT 1,
            UNIQUE(chat_id, user_id, message_date) ON CONFLICT REPLACE
        )
    """)

    # ===== TAQIQLANGAN SO'ZLAR =====
    await db.execute("""
        CREATE TABLE IF NOT EXISTS badwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            added_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(chat_id, word) ON CONFLICT IGNORE
        )
    """)

    await db.commit()
    logger.info("Baza sxemasi muvaffaqiyatli yaratildi.")
