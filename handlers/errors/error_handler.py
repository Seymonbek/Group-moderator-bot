import logging

from aiogram.utils.exceptions import (
    Unauthorized,
    InvalidQueryID,
    TelegramAPIError,
    CantDemoteChatCreator,
    MessageNotModified,
    MessageToDeleteNotFound,
    MessageTextIsEmpty,
    RetryAfter,
    CantParseEntities,
    MessageCantBeDeleted,
)

from loader import dp

logger = logging.getLogger(__name__)


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Global xatolik ushlash handleri.
    Barcha kutilmagan xatoliklarni log qiladi va botning to'xtab qolishini oldini oladi.
    """

    # Xavfsiz xatoliklar — log qilamiz, lekin foydalanuvchiga ko'rsatmaymiz
    SAFE_EXCEPTIONS = (
        MessageNotModified,
        MessageCantBeDeleted,
        MessageToDeleteNotFound,
        MessageTextIsEmpty,
        CantDemoteChatCreator,
    )

    if isinstance(exception, SAFE_EXCEPTIONS):
        logger.warning(f"Xavfsiz xatolik: {type(exception).__name__}: {exception}")
        return True

    if isinstance(exception, Unauthorized):
        logger.error(f"Avtorizatsiya xatoligi: {exception}")
        return True

    if isinstance(exception, InvalidQueryID):
        logger.error(f"Noto'g'ri callback query: {exception}")
        return True

    if isinstance(exception, RetryAfter):
        logger.warning(f"Telegram flood cheklovi: {exception.timeout} soniya kutish kerak")
        return True

    if isinstance(exception, CantParseEntities):
        logger.error(f"HTML/Markdown tahlil xatoligi: {exception}")
        return True

    if isinstance(exception, TelegramAPIError):
        logger.error(f"Telegram API xatoligi: {exception}")
        return True

    # Kutilmagan xatoliklar
    logger.exception(f"Kutilmagan xatolik!\nUpdate: {update}\nException: {exception}")
    return True
