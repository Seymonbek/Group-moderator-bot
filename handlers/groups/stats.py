"""
Guruh statistikasi — xabar soni, faol a'zolar.
"""
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from core.filters import IsGroup, AdminFilter
from core.database.models import get_today_stats, get_total_messages_today
from loader import dp, bot

logger = logging.getLogger(__name__)


@dp.message_handler(IsGroup(), Command("stats", prefixes="!/"), AdminFilter())
async def show_stats(message: types.Message):
    """Guruh statistikasini ko'rsatadi."""
    chat_id = message.chat.id

    total_today = await get_total_messages_today(chat_id)
    top_users = await get_today_stats(chat_id, limit=10)

    # Guruh a'zolari soni
    try:
        members_count = await bot.get_chat_members_count(chat_id)
    except Exception:
        members_count = "?"

    text = (
        f"📊 <b>{message.chat.title}</b> — Statistika\n\n"
        f"👥 A'zolar soni: <b>{members_count}</b>\n"
        f"💬 Bugungi xabarlar: <b>{total_today}</b>\n"
    )

    if top_users:
        text += "\n🏆 <b>Bugungi eng faol a'zolar:</b>\n\n"
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for i, user in enumerate(top_users):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            text += f"  {medal} {user['user_name']} — <b>{user['msg_count']}</b> xabar\n"
    else:
        text += "\nℹ️ Bugun hali xabar yozilmagan."

    await message.answer(text)
