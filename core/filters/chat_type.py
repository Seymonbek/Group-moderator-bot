from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsGroup(BoundFilter):
    """Xabar guruhdan kelganligini tekshiruvchi filtr."""

    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )


class IsPrivate(BoundFilter):
    """Xabar shaxsiy chatdan kelganligini tekshiruvchi filtr."""

    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
