"""
Avtomatik moderatsiya handlerlari.

MUHIM: Aiogram v2 da bir xil filter'li bir nechta handler
ro'yxatdan o'tkazilsa, faqat BIRINCHISI ishlaydi.
Shuning uchun barcha TEXT tekshiruvlari BITTA handler ichida
amalga oshiriladi.
"""
import asyncio
import logging
import re
import unicodedata

from aiogram import types
from aiogram.dispatcher.filters import Command

from core.filters import IsGroup, AdminFilter
from core.database.models import (
    get_group_settings, get_badwords, add_badword, remove_badword,
    log_action, add_warn, reset_warns,
)
from core.utils.message_manager import auto_clean
from loader import dp, bot

logger = logging.getLogger(__name__)

# =============================================
#  YORDAMCHI FUNKSIYALAR
# =============================================

LINK_PATTERN = re.compile(
    r"(https?://|t\.me/|@\w{5,}|bit\.ly/|goo\.gl/|telegra\.ph/)",
    re.IGNORECASE,
)


def _is_mostly_arabic(text: str, threshold: float = 0.5) -> bool:
    """Matnning ko'p qismi arab yozuvida ekanligini tekshiradi."""
    if not text:
        return False
    arabic_count = sum(
        1 for ch in text if unicodedata.category(ch).startswith("Lo")
        and "ARABIC" in unicodedata.name(ch, "")
    )
    return arabic_count / max(len(text.strip()), 1) > threshold


def _is_emoji_spam(text: str, threshold: float = 0.7) -> bool:
    """Matnning 70%+ qismi emoji ekanligini tekshiradi."""
    if not text or len(text) < 5:
        return False
    emoji_count = sum(
        1 for ch in text if unicodedata.category(ch) in ("So", "Sk", "Sc", "Sm")
        or "\U0001F600" <= ch <= "\U0001FAFF"
        or "\U00002702" <= ch <= "\U000027B0"
    )
    return emoji_count / max(len(text.strip()), 1) > threshold


async def _is_admin(message: types.Message) -> bool:
    """Foydalanuvchi admin yoki yo'qligini tekshiradi."""
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()
    except Exception:
        return False


# =============================================
#  BITTA MARKAZIY TEXT HANDLER
#  (Aiogram v2 da bir xil filter'li birinchi
#   handler ishlaydi, shuning uchun birlashtirdik)
# =============================================

@dp.message_handler(IsGroup(), content_types=types.ContentTypes.TEXT, state="*")
async def auto_moderation_text_handler(message: types.Message):
    """
    Barcha matnli xabarlarni tekshiruvchi yagona handler.
    Tekshiruv tartibi: forward → link → bad words → arabic → emoji
    """
    if await _is_admin(message):
        return

    settings = await get_group_settings(message.chat.id)
    text = message.text or ""

    # 1. ANTI-FORWARD: forward xabarlarni tekshirish
    if settings["anti_forward"] and (message.forward_from or message.forward_from_chat):
        try:
            await message.delete()
            await log_action(
                chat_id=message.chat.id, action="auto_delete_forward",
                user_id=message.from_user.id, user_name=message.from_user.full_name,
            )
            warn_msg = await message.answer(
                f"🔄 <b>{message.from_user.full_name}</b>, guruhda forward qilish taqiqlangan!"
            )
            asyncio.create_task(auto_clean(warn_msg))
        except Exception as e:
            logger.error(f"Anti-forward xatoligi: {e}")
        return  # Xabar o'chirildi, davom etishga hojat yo'q

    # 2. ANTI-LINK: havola tekshirish
    if settings["anti_link"] and LINK_PATTERN.search(text):
        try:
            await message.delete()
            await log_action(
                chat_id=message.chat.id, action="auto_delete_link",
                user_id=message.from_user.id, user_name=message.from_user.full_name,
            )
            warn_msg = await message.answer(
                f"🔗 <b>{message.from_user.full_name}</b>, guruhda havola yuborish taqiqlangan!"
            )
            asyncio.create_task(auto_clean(warn_msg))
        except Exception as e:
            logger.error(f"Anti-link xatoligi: {e}")
        return

    # 3. BAD WORDS: taqiqlangan so'zlar tekshirish
    if settings["bad_words_enabled"]:
        badwords = await get_badwords(message.chat.id)
        if badwords:
            text_lower = text.lower()
            for word in badwords:
                if word in text_lower:
                    try:
                        await message.delete()
                        warn_count = await add_warn(
                            chat_id=message.chat.id,
                            user_id=message.from_user.id,
                            user_name=message.from_user.full_name,
                            reason=f"Taqiqlangan so'z: {word}",
                        )
                        await log_action(
                            chat_id=message.chat.id, action="auto_warn_badword",
                            user_id=message.from_user.id, user_name=message.from_user.full_name,
                            reason=f"Taqiqlangan so'z: {word}",
                        )
                        max_warns = settings["max_warns"]
                        if warn_count >= max_warns:
                            await message.chat.kick(user_id=message.from_user.id)
                            await reset_warns(message.chat.id, message.from_user.id)
                            warn_msg = await message.answer(
                                f"🔨 <b>{message.from_user.full_name}</b> taqiqlangan so'z ishlatgani va "
                                f"{max_warns} ta ogohlantirish to'plangani sababli guruhdan haydaldi!"
                            )
                        else:
                            warn_msg = await message.answer(
                                f"⚠️ <b>{message.from_user.full_name}</b>, taqiqlangan so'z ishlatish mumkin emas!\n"
                                f"📊 Ogohlantirish: {warn_count}/{max_warns}"
                            )
                        asyncio.create_task(auto_clean(warn_msg))
                    except Exception as e:
                        logger.error(f"Bad words xatoligi: {e}")
                    return  # Birinchi topilgan so'zdan keyin to'xtaymiz

    # 4. ANTI-ARABIC: arab yozuvi tekshirish
    if settings["anti_arabic"] and _is_mostly_arabic(text):
        try:
            await message.delete()
            await log_action(
                chat_id=message.chat.id, action="auto_delete_arabic",
                user_id=message.from_user.id, user_name=message.from_user.full_name,
            )
            warn_msg = await message.answer(
                f"🚫 <b>{message.from_user.full_name}</b>, arab yozuvidagi xabarlar taqiqlangan!"
            )
            asyncio.create_task(auto_clean(warn_msg))
        except Exception as e:
            logger.error(f"Anti-arabic xatoligi: {e}")
        return

    # 5. ANTI-EMOJI SPAM: emoji spamni tekshirish
    if settings["anti_emoji_spam"] and _is_emoji_spam(text):
        try:
            await message.delete()
            await log_action(
                chat_id=message.chat.id, action="auto_delete_emoji",
                user_id=message.from_user.id, user_name=message.from_user.full_name,
            )
            warn_msg = await message.answer(
                f"🚫 <b>{message.from_user.full_name}</b>, emoji spam taqiqlangan!"
            )
            asyncio.create_task(auto_clean(warn_msg))
        except Exception as e:
            logger.error(f"Anti-emoji xatoligi: {e}")


# =============================================
#  ANTI-FORWARD (matndan boshqa kontentlar uchun)
# =============================================

@dp.message_handler(IsGroup(), content_types=types.ContentTypes.ANY, state="*")
async def auto_moderation_non_text_forward(message: types.Message):
    """
    Matndan boshqa turdagi forward xabarlarni o'chiradi
    (rasm, video, audio va h.k.).
    """
    # Faqat forward xabarlarni tekshiramiz
    if not message.forward_from and not message.forward_from_chat:
        return

    if await _is_admin(message):
        return

    settings = await get_group_settings(message.chat.id)
    if not settings["anti_forward"]:
        return

    try:
        await message.delete()
        await log_action(
            chat_id=message.chat.id, action="auto_delete_forward",
            user_id=message.from_user.id, user_name=message.from_user.full_name,
        )
        warn_msg = await message.answer(
            f"🔄 <b>{message.from_user.full_name}</b>, guruhda forward qilish taqiqlangan!"
        )
        asyncio.create_task(auto_clean(warn_msg))
    except Exception as e:
        logger.error(f"Anti-forward xatoligi: {e}")


# =============================================
#  BAD WORDS BOSHQARUVI (admin buyruqlari)
# =============================================

@dp.message_handler(IsGroup(), Command("addword", prefixes="!/"), AdminFilter())
async def add_bad_word(message: types.Message):
    """Taqiqlangan so'z qo'shish. Ishlatilishi: /addword so'z"""
    word = message.get_args()
    if not word:
        await message.reply("⚠️ Ishlatilishi: /addword <so'z>")
        return

    added = await add_badword(message.chat.id, word, message.from_user.id)
    if added:
        await message.reply(f"✅ <b>{word}</b> taqiqlangan so'zlar ro'yxatiga qo'shildi.")
    else:
        await message.reply(f"ℹ️ <b>{word}</b> allaqachon ro'yxatda mavjud.")


@dp.message_handler(IsGroup(), Command("delword", prefixes="!/"), AdminFilter())
async def del_bad_word(message: types.Message):
    """Taqiqlangan so'zni o'chirish. Ishlatilishi: /delword so'z"""
    word = message.get_args()
    if not word:
        await message.reply("⚠️ Ishlatilishi: /delword <so'z>")
        return

    removed = await remove_badword(message.chat.id, word)
    if removed:
        await message.reply(f"✅ <b>{word}</b> taqiqlangan so'zlar ro'yxatidan o'chirildi.")
    else:
        await message.reply(f"ℹ️ <b>{word}</b> ro'yxatda topilmadi.")


@dp.message_handler(IsGroup(), Command("badwords", prefixes="!/"), AdminFilter())
async def list_bad_words(message: types.Message):
    """Taqiqlangan so'zlar ro'yxatini ko'rsatish."""
    words = await get_badwords(message.chat.id)
    if not words:
        await message.reply("📝 Taqiqlangan so'zlar ro'yxati bo'sh.")
        return

    text = "📝 <b>Taqiqlangan so'zlar:</b>\n\n"
    for i, word in enumerate(words, 1):
        text += f"  {i}. <code>{word}</code>\n"

    await message.reply(text)
