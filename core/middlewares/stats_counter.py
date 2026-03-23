"""
Har bir guruh xabarini hisoblab, bazaga yozuvchi middleware.
/stats buyrug'i uchun statistika to'playdi.
"""
import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from core.database.models import increment_message_count

logger = logging.getLogger(__name__)


class StatsCounterMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.type not in (types.ChatType.GROUP, types.ChatType.SUPERGROUP):
            return

        # Bot xabarlarini hisoblamaymiz
        if message.from_user.is_bot:
            return

        try:
            await increment_message_count(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                user_name=message.from_user.full_name,
            )
        except Exception as e:
            logger.error(f"Statistika yozishda xatolik: {e}")
