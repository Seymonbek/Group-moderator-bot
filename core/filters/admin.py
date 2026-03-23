import logging

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

logger = logging.getLogger(__name__)


class AdminFilter(BoundFilter):
    """Foydalanuvchi guruh admini ekanligini tekshiruvchi filtr."""

    async def check(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()
