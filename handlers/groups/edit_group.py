import io
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from core.filters import IsGroup, AdminFilter
from loader import dp, bot

logger = logging.getLogger(__name__)


@dp.message_handler(IsGroup(), Command("set_photo", prefixes="!/"), AdminFilter())
async def set_new_photo(message: types.Message):
    """Guruh rasmini reply qilingan rasmdagi rasm bilan almashtiradi."""
    reply = message.reply_to_message
    if not reply or not reply.photo:
        await message.reply("⚠️ Rasm o'rnatish uchun birorta rasmga reply qiling!")
        return

    try:
        photo = reply.photo[-1]
        photo_file = await photo.download(destination=io.BytesIO())
        input_file = types.InputFile(photo_file)
        await message.chat.set_photo(photo=input_file)
        await message.reply("✅ Guruh rasmi muvaffaqiyatli o'zgartirildi!")
    except Exception as err:
        logger.error(f"set_photo buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")


@dp.message_handler(IsGroup(), Command("set_title", prefixes="!/"), AdminFilter())
async def set_new_title(message: types.Message):
    """Guruh nomini reply qilingan xabardagi matn bilan almashtiradi."""
    reply = message.reply_to_message
    if not reply or not reply.text:
        await message.reply("⚠️ Nom o'rnatish uchun birorta matnli xabarga reply qiling!")
        return

    try:
        await bot.set_chat_title(message.chat.id, title=reply.text)
        await message.reply(f"✅ Guruh nomi o'zgartirildi: <b>{reply.text}</b>")
    except Exception as err:
        logger.error(f"set_title buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")


@dp.message_handler(IsGroup(), Command("set_description", prefixes="!/"), AdminFilter())
async def set_new_description(message: types.Message):
    """Guruh tavsifini reply qilingan xabardagi matn bilan almashtiradi."""
    reply = message.reply_to_message
    if not reply or not reply.text:
        await message.reply("⚠️ Tavsif o'rnatish uchun birorta matnli xabarga reply qiling!")
        return

    try:
        await message.chat.set_description(description=reply.text)
        await message.reply("✅ Guruh tavsifi muvaffaqiyatli o'zgartirildi!")
    except Exception as err:
        logger.error(f"set_description buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")
