from aiogram import types

from core.filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), state=None)
async def bot_echo(message: types.Message):
    """Shaxsiy chatdagi noma'lum xabarlarga javob beradi."""
    await message.answer(
        "🤖 Kechirasiz, bu buyruqni tushunmadim.\n"
        "Yordam uchun /help ni bosing."
    )
