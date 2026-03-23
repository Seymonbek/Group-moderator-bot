"""
Admin sozlamalari paneli — inline tugmalar bilan boshqaruv.
/settings buyrug'i orqali barcha sozlamalarni on/off qilish mumkin.
"""
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.filters import IsGroup, AdminFilter
from core.database.models import get_group_settings, toggle_group_setting, update_group_setting
from loader import dp

logger = logging.getLogger(__name__)

# Sozlamalar ro'yxati: (baza_kalit, emoji, nomi)
SETTINGS_MAP = [
    ("anti_link", "🔗", "Anti-link"),
    ("anti_flood", "🌊", "Anti-flood"),
    ("anti_bot", "🤖", "Anti-bot"),
    ("anti_forward", "🔄", "Anti-forward"),
    ("anti_arabic", "🔤", "Anti-arabic"),
    ("anti_emoji_spam", "😀", "Anti-emoji spam"),
    ("bad_words_enabled", "🤬", "So'z filtri"),
    ("captcha_enabled", "🔢", "Captcha"),
    ("auto_delete_joins", "🧹", "Auto-delete join/leave"),
]


def _build_settings_keyboard(settings: dict) -> InlineKeyboardMarkup:
    """Sozlamalar paneli uchun inline keyboard yaratadi."""
    keyboard = InlineKeyboardMarkup(row_width=1)

    for key, emoji, name in SETTINGS_MAP:
        status = "✅" if settings.get(key) else "❌"
        keyboard.add(
            InlineKeyboardButton(
                text=f"{emoji} {name}: {status}",
                callback_data=f"settings:{key}",
            )
        )

    # Til sozlamasi
    lang = settings.get("language", "uz")
    lang_names = {"uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Ruscha", "en": "🇬🇧 English"}
    keyboard.add(
        InlineKeyboardButton(
            text=f"🌐 Til: {lang_names.get(lang, lang)}",
            callback_data="settings:language",
        )
    )

    keyboard.add(
        InlineKeyboardButton(text="❌ Yopish", callback_data="settings:close")
    )

    return keyboard


@dp.message_handler(IsGroup(), Command("settings", prefixes="!/"), AdminFilter())
async def show_settings(message: types.Message):
    """Guruh sozlamalari panelini ko'rsatadi."""
    settings = await get_group_settings(message.chat.id)
    keyboard = _build_settings_keyboard(settings)

    await message.answer(
        f"⚙️ <b>{message.chat.title}</b> — Sozlamalar\n\n"
        f"Sozlamalarni on/off qilish uchun tugmalarni bosing:",
        reply_markup=keyboard,
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("settings:"))
async def settings_callback(callback: types.CallbackQuery):
    """Sozlamalar tugmasi bosilganda."""
    # Admin tekshiruvi
    try:
        member = await callback.message.chat.get_member(callback.from_user.id)
        if not member.is_chat_admin():
            await callback.answer("⛔ Faqat adminlar sozlamalarni o'zgartira oladi!", show_alert=True)
            return
    except Exception:
        await callback.answer("Xatolik!", show_alert=True)
        return

    key = callback.data.split(":")[1]

    if key == "close":
        await callback.message.delete()
        await callback.answer()
        return

    if key == "language":
        # Tilni aylantiramiz: uz -> ru -> en -> uz
        settings = await get_group_settings(callback.message.chat.id)
        current = settings.get("language", "uz")
        lang_cycle = {"uz": "ru", "ru": "en", "en": "uz"}
        new_lang = lang_cycle.get(current, "uz")
        await update_group_setting(callback.message.chat.id, "language", new_lang)
        lang_names = {"uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Ruscha", "en": "🇬🇧 English"}
        await callback.answer(f"Til o'zgartirildi: {lang_names[new_lang]}")
    else:
        # On/off toggle
        new_state = await toggle_group_setting(callback.message.chat.id, key)
        status = "yoqildi ✅" if new_state else "o'chirildi ❌"
        # Sozlama nomini topamiz
        name = key
        for k, emoji, n in SETTINGS_MAP:
            if k == key:
                name = n
                break
        await callback.answer(f"{name} {status}")

    # Panelni yangilaymiz
    settings = await get_group_settings(callback.message.chat.id)
    keyboard = _build_settings_keyboard(settings)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass
