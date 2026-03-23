import logging

from aiogram import Dispatcher

from data.config import ADMINS

logger = logging.getLogger(__name__)


async def on_startup_notify(dp: Dispatcher):
    """Bot ishga tushganda barcha adminlarga xabar yuboradi."""
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "✅ Bot ishga tushdi va tayyor!")
        except Exception as err:
            logger.exception(f"Admin {admin} ga xabar yuborishda xatolik: {err}")
