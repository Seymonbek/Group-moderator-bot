"""
Anti-flood middleware — tez-tez xabar yozuvchi foydalanuvchilarni aniqlaydi.
Har bir guruh uchun alohida sozlanadi (flood_limit, flood_time).
"""
import datetime
import logging
import time
from collections import defaultdict

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from core.database.models import get_group_settings, log_action

logger = logging.getLogger(__name__)


class AntiFloodMiddleware(BaseMiddleware):
    """
    Anti-flood middleware.
    Foydalanuvchi belgilangan vaqt ichida belgilangan sondan ko'p xabar yozsa,
    avtomatik mute qilinadi.
    """

    def __init__(self):
        super().__init__()
        # {(chat_id, user_id): [timestamp1, timestamp2, ...]}
        self._messages: dict[tuple[int, int], list[float]] = defaultdict(list)

    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.type not in (types.ChatType.GROUP, types.ChatType.SUPERGROUP):
            return

        # Admin tekshiruvi — adminlar cheklanmaydi
        try:
            member = await message.chat.get_member(message.from_user.id)
            if member.is_chat_admin():
                return
        except Exception:
            return

        settings = await get_group_settings(message.chat.id)
        if not settings["anti_flood"]:
            return

        flood_limit = settings["flood_limit"]   # standart: 5 xabar
        flood_time = settings["flood_time"]      # standart: 10 soniya

        key = (message.chat.id, message.from_user.id)
        now = time.time()

        # Eski xabarlarni tozalash
        self._messages[key] = [
            t for t in self._messages[key] if now - t < flood_time
        ]
        self._messages[key].append(now)

        if len(self._messages[key]) > flood_limit:
            # Flood aniqlandi — mute qilish
            self._messages[key].clear()
            try:
                until = datetime.datetime.now() + datetime.timedelta(minutes=5)
                await message.chat.restrict(
                    user_id=message.from_user.id,
                    can_send_messages=False,
                    until_date=until,
                )
                await log_action(
                    chat_id=message.chat.id,
                    action="auto_mute_flood",
                    user_id=message.from_user.id,
                    user_name=message.from_user.full_name,
                    reason=f"Flood: {flood_limit}+ xabar / {flood_time} soniya",
                )
                await message.answer(
                    f"🚫 <b>{message.from_user.full_name}</b> flood sababli 5 daqiqa mute qilindi!"
                )
            except Exception as e:
                logger.error(f"Anti-flood mute xatoligi: {e}")
            raise CancelHandler()
