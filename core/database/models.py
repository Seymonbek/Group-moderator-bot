"""
Baza bilan ishlash uchun yordamchi funksiyalar (CRUD operatsiyalari).
Barcha handler'lar shu funksiyalar orqali bazaga murojaat qiladi.
"""
import logging
from datetime import date
from typing import Optional

from core.database.connection import get_db

logger = logging.getLogger(__name__)


# ╔══════════════════════════════════════════╗
# ║         GURUH SOZLAMALARI                ║
# ╚══════════════════════════════════════════╝

async def get_group_settings(chat_id: int) -> dict:
    """Guruh sozlamalarini qaytaradi. Agar yo'q bo'lsa, standart sozlamalar bilan yaratadi."""
    db = await get_db()
    cursor = await db.execute("SELECT * FROM groups WHERE chat_id = ?", (chat_id,))
    row = await cursor.fetchone()

    if row is None:
        await db.execute("INSERT INTO groups (chat_id) VALUES (?)", (chat_id,))
        await db.commit()
        cursor = await db.execute("SELECT * FROM groups WHERE chat_id = ?", (chat_id,))
        row = await cursor.fetchone()

    return dict(row)


async def update_group_setting(chat_id: int, key: str, value) -> None:
    """Guruh sozlamasini yangilaydi."""
    db = await get_db()
    # Avval guruh mavjudligini tekshiramiz
    await get_group_settings(chat_id)
    await db.execute(f"UPDATE groups SET {key} = ? WHERE chat_id = ?", (value, chat_id))
    await db.commit()


async def toggle_group_setting(chat_id: int, key: str) -> bool:
    """Sozlamani on/off qiladi. Yangi holatni qaytaradi (True = yoqildi)."""
    settings = await get_group_settings(chat_id)
    new_value = 0 if settings[key] else 1
    await update_group_setting(chat_id, key, new_value)
    return bool(new_value)


# ╔══════════════════════════════════════════╗
# ║         WARN (OGOHLANTIRISH)             ║
# ╚══════════════════════════════════════════╝

async def add_warn(
    chat_id: int,
    user_id: int,
    user_name: str,
    reason: Optional[str] = None,
    admin_id: Optional[int] = None,
    admin_name: Optional[str] = None,
) -> int:
    """
    Ogohlantirish qo'shadi.
    Qaytaradi: foydalanuvchining joriy ogohlantirshlar soni.
    """
    db = await get_db()
    await db.execute(
        "INSERT INTO warns (chat_id, user_id, user_name, reason, admin_id, admin_name) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (chat_id, user_id, user_name, reason, admin_id, admin_name),
    )
    await db.commit()
    return await get_warn_count(chat_id, user_id)


async def get_warn_count(chat_id: int, user_id: int) -> int:
    """Foydalanuvchining ogohlantirshlar sonini qaytaradi."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT COUNT(*) FROM warns WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    row = await cursor.fetchone()
    return row[0]


async def get_warns(chat_id: int, user_id: int) -> list:
    """Foydalanuvchining barcha ogohlantirshlarini qaytaradi."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM warns WHERE chat_id = ? AND user_id = ? ORDER BY created_at DESC",
        (chat_id, user_id),
    )
    return [dict(row) for row in await cursor.fetchall()]


async def remove_last_warn(chat_id: int, user_id: int) -> bool:
    """Oxirgi ogohlantirshni o'chiradi. True qaytaradi agar o'chirilgan bo'lsa."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT id FROM warns WHERE chat_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1",
        (chat_id, user_id),
    )
    row = await cursor.fetchone()
    if row is None:
        return False
    await db.execute("DELETE FROM warns WHERE id = ?", (row[0],))
    await db.commit()
    return True


async def reset_warns(chat_id: int, user_id: int) -> int:
    """Foydalanuvchining barcha ogohlantirshlarini o'chiradi. O'chirilganlar sonini qaytaradi."""
    db = await get_db()
    cursor = await db.execute(
        "DELETE FROM warns WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    await db.commit()
    return cursor.rowcount


# ╔══════════════════════════════════════════╗
# ║         MODERATSIYA TARIXI (LOG)         ║
# ╚══════════════════════════════════════════╝

async def log_action(
    chat_id: int,
    action: str,
    user_id: int = None,
    user_name: str = None,
    admin_id: int = None,
    admin_name: str = None,
    reason: str = None,
) -> None:
    """Moderatsiya harakatini bazaga yozadi."""
    db = await get_db()
    await db.execute(
        "INSERT INTO actions_log (chat_id, action, user_id, user_name, admin_id, admin_name, reason) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (chat_id, action, user_id, user_name, admin_id, admin_name, reason),
    )
    await db.commit()


async def get_action_log(chat_id: int, limit: int = 10) -> list:
    """Oxirgi N ta moderatsiya harakatlarini qaytaradi."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM actions_log WHERE chat_id = ? ORDER BY created_at DESC LIMIT ?",
        (chat_id, limit),
    )
    return [dict(row) for row in await cursor.fetchall()]


# ╔══════════════════════════════════════════╗
# ║         STATISTIKA                       ║
# ╚══════════════════════════════════════════╝

async def increment_message_count(chat_id: int, user_id: int, user_name: str) -> None:
    """Foydalanuvchining bugungi xabar sonini 1 ga oshiradi."""
    db = await get_db()
    today = date.today().isoformat()
    await db.execute(
        """
        INSERT INTO stats (chat_id, user_id, user_name, message_date, msg_count)
        VALUES (?, ?, ?, ?, 1)
        ON CONFLICT(chat_id, user_id, message_date)
        DO UPDATE SET msg_count = msg_count + 1, user_name = ?
        """,
        (chat_id, user_id, user_name, today, user_name),
    )
    await db.commit()


async def get_today_stats(chat_id: int, limit: int = 5) -> list:
    """Bugungi eng faol foydalanuvchilar ro'yxatini qaytaradi."""
    db = await get_db()
    today = date.today().isoformat()
    cursor = await db.execute(
        """
        SELECT user_id, user_name, msg_count
        FROM stats
        WHERE chat_id = ? AND message_date = ?
        ORDER BY msg_count DESC
        LIMIT ?
        """,
        (chat_id, today, limit),
    )
    return [dict(row) for row in await cursor.fetchall()]


async def get_total_messages_today(chat_id: int) -> int:
    """Bugungi jami xabar sonini qaytaradi."""
    db = await get_db()
    today = date.today().isoformat()
    cursor = await db.execute(
        "SELECT COALESCE(SUM(msg_count), 0) FROM stats WHERE chat_id = ? AND message_date = ?",
        (chat_id, today),
    )
    row = await cursor.fetchone()
    return row[0]


# ╔══════════════════════════════════════════╗
# ║         TAQIQLANGAN SO'ZLAR              ║
# ╚══════════════════════════════════════════╝

async def add_badword(chat_id: int, word: str, added_by: int = None) -> bool:
    """Taqiqlangan so'z qo'shadi. True = muvaffaqiyatli, False = allaqachon mavjud."""
    db = await get_db()
    cursor = await db.execute(
        "INSERT OR IGNORE INTO badwords (chat_id, word, added_by) VALUES (?, ?, ?)",
        (chat_id, word.lower().strip(), added_by),
    )
    await db.commit()
    return cursor.rowcount > 0


async def remove_badword(chat_id: int, word: str) -> bool:
    """Taqiqlangan so'zni o'chiradi."""
    db = await get_db()
    cursor = await db.execute(
        "DELETE FROM badwords WHERE chat_id = ? AND word = ?",
        (chat_id, word.lower().strip()),
    )
    await db.commit()
    return cursor.rowcount > 0


async def get_badwords(chat_id: int) -> list[str]:
    """Guruhning taqiqlangan so'zlar ro'yxatini qaytaradi."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT word FROM badwords WHERE chat_id = ?", (chat_id,)
    )
    rows = await cursor.fetchall()
    return [row[0] for row in rows]
