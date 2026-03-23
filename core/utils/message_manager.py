import asyncio
import logging

from aiogram import types

logger = logging.getLogger(__name__)

# Xabarni o'chirishdan oldin kutish vaqti (sekundlarda)
AUTO_DELETE_DELAY = 5


async def delete_after(message: types.Message, delay: int = AUTO_DELETE_DELAY):
    """
    Berilgan xabarni `delay` soniyadan keyin o'chiradi.
    asyncio.create_task() orqali chaqirilganda, asosiy oqimni bloklamaydi.
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Xabarni o'chirishda xatolik: {e}")


async def auto_clean(*messages: types.Message, delay: int = AUTO_DELETE_DELAY):
    """
    Bir nechta xabarni bir vaqtda `delay` soniyadan keyin o'chiradi.
    Ishlatilishi:
        asyncio.create_task(auto_clean(msg1, msg2, msg3))
    """
    await asyncio.sleep(delay)
    for msg in messages:
        try:
            await msg.delete()
        except Exception as e:
            logger.warning(f"Xabarni o'chirishda xatolik (id={msg.message_id}): {e}")


async def notify_and_clean(
    message: types.Message,
    text: str,
    delay: int = AUTO_DELETE_DELAY,
):
    """
    Javob xabarini yuboradi va keyin barcha tegishli xabarlarni o'chiradi.
    Bu funksiya moderatsiya buyruqlarida takroriy kod yozmaslik uchun yaratilgan.
    """
    service_msg = await message.answer(text)
    asyncio.create_task(auto_clean(message, service_msg, delay=delay))
