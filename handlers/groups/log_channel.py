"""
Log kanal boshqaruvi.
Barcha moderatsiya harakatlari log kanalga yuboriladi.
"""
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from core.filters import IsGroup, AdminFilter
from core.database.models import get_group_settings, update_group_setting
from loader import dp, bot

logger = logging.getLogger(__name__)


@dp.message_handler(IsGroup(), Command("setlog", prefixes="!/"), AdminFilter())
async def set_log_channel(message: types.Message):
    """
    Log kanalini sozlash.
    Ishlatilishi: Kanalga xabar yuboring, keyin guruhda shu xabarga reply qilib /setlog yozing.
    Yoki: /setlog <kanal_id>
    """
    args = message.get_args()

    if args:
        try:
            channel_id = int(args)
        except ValueError:
            await message.reply("⚠️ Noto'g'ri kanal ID. Raqam kiriting.")
            return
    elif message.reply_to_message and message.reply_to_message.forward_from_chat:
        channel_id = message.reply_to_message.forward_from_chat.id
    else:
        await message.reply(
            "⚠️ Ishlatilishi:\n"
            "1. Kanaldan forward qilingan xabarga reply qilib /setlog yozing\n"
            "2. Yoki: /setlog <kanal_id>"
        )
        return

    # Kanalga yozish huquqini tekshirish
    try:
        test_msg = await bot.send_message(channel_id, "✅ Log kanal muvaffaqiyatli ulandi!")
        await test_msg.delete()
    except Exception as err:
        await message.reply(
            f"❌ Kanalga yozib bo'lmadi! Botni kanalga admin qilib qo'shing.\n"
            f"Xatolik: {err}"
        )
        return

    await update_group_setting(message.chat.id, "log_channel_id", channel_id)
    await message.reply(f"✅ Log kanal sozlandi: <code>{channel_id}</code>")


@dp.message_handler(IsGroup(), Command("unsetlog", prefixes="!/"), AdminFilter())
async def unset_log_channel(message: types.Message):
    """Log kanalini o'chirish."""
    await update_group_setting(message.chat.id, "log_channel_id", None)
    await message.reply("✅ Log kanal o'chirildi.")


async def send_log(chat_id: int, text: str):
    """Log kanalga xabar yuborish."""
    try:
        settings = await get_group_settings(chat_id)
        log_channel = settings.get("log_channel_id")
        if log_channel:
            await bot.send_message(log_channel, text)
    except Exception as e:
        logger.error(f"Log kanalga yozishda xatolik: {e}")
