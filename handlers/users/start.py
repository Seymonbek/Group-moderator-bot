from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from core.filters import IsGroup, IsPrivate
from loader import dp


@dp.message_handler(IsGroup(), CommandStart())
async def bot_start_group(message: types.Message):
    """Guruhda /start buyrug'iga javob."""
    await message.answer(
        f"👋 Salom, {message.from_user.full_name}!\n"
        f"Men bu guruhning moderator botiman."
    )


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start_private(message: types.Message):
    """Shaxsiy chatda /start buyrug'iga javob."""
    await message.answer(
        f"👋 Salom, {message.from_user.full_name}!\n"
        f"Men guruhlarni boshqarish uchun yaratilgan moderator botiman.\n\n"
        f"Buyruqlar ro'yxatini ko'rish uchun /help ni bosing."
    )
