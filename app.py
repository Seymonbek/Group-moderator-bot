import logging

from aiogram import Dispatcher, executor

from loader import dp, bot
from core.database import init_db, close_db
from core.filters import setup as setup_filters
from core.middlewares import setup as setup_middlewares
from core.utils.bot_commands import set_default_commands
from core.utils.notify_admins import on_startup_notify

# Handler'larni import qilish (ro'yxatdan o'tkazish uchun)
import handlers

# Logging sozlamalari
logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def on_startup(dispatcher: Dispatcher):
    """Bot ishga tushganda bajariladigan vazifalar."""
    # Ma'lumotlar bazasini ishga tushirish
    await init_db()

    # Filtrlarni ro'yxatdan o'tkazish
    setup_filters(dp)

    # Middleware'larni ulash
    setup_middlewares(dp)

    # Standart buyruqlarni o'rnatish (/start, /help, ...)
    await set_default_commands(dispatcher)

    # Adminlarga xabar yuborish
    await on_startup_notify(dispatcher)

    logger.info("Bot muvaffaqiyatli ishga tushdi!")


async def on_shutdown(dispatcher: Dispatcher):
    """Bot to'xtaganda bajariladigan vazifalar."""
    await close_db()
    logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
