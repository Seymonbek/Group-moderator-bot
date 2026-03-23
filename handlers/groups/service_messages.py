"""
Xizmat xabarlari: yangi a'zo, tark etish, welcome, captcha, anti-bot.

MUHIM: Aiogram v2 da bitta content_type uchun faqat BIRINCHI
mos handler ishlaydi. Shuning uchun NEW_CHAT_MEMBERS va
LEFT_CHAT_MEMBER uchun BARCHA mantiq shu faylda birlashtirilgan.
"""
import asyncio
import logging
import random

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.filters import IsGroup, AdminFilter
from core.database.models import get_group_settings, update_group_setting, log_action
from core.utils.message_manager import auto_clean
from loader import dp, bot

logger = logging.getLogger(__name__)

# =============================================
#  CAPTCHA YORDAMCHI FUNKSIYALARI
# =============================================

# Kutilayotgan captcha javoblari: {(chat_id, user_id): {"answer": int, "msg_id": int}}
_pending_captcha: dict[tuple[int, int], dict] = {}


def _generate_captcha() -> tuple[str, int]:
    """Oddiy matematik misol yaratadi."""
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(["+", "-"])
    if op == "+":
        answer = a + b
    else:
        if a < b:
            a, b = b, a
        answer = a - b
    return f"{a} {op} {b}", answer


def _create_captcha_keyboard(answer: int) -> InlineKeyboardMarkup:
    """Captcha uchun 4 ta variantli inline tugmalar yaratadi."""
    options = {answer}
    while len(options) < 4:
        fake = answer + random.randint(-5, 5)
        if fake != answer and fake >= 0:
            options.add(fake)

    buttons = [
        InlineKeyboardButton(text=str(opt), callback_data=f"captcha:{opt}")
        for opt in sorted(options)
    ]
    return InlineKeyboardMarkup(row_width=4).add(*buttons)


async def _captcha_timeout(chat_id: int, user_id: int, timeout: int):
    """Vaqt tugasa, foydalanuvchini kick qiladi."""
    await asyncio.sleep(timeout)
    key = (chat_id, user_id)
    if key in _pending_captcha:
        del _pending_captcha[key]
        try:
            await bot.kick_chat_member(chat_id, user_id)
            await bot.unban_chat_member(chat_id, user_id)
            await bot.send_message(
                chat_id,
                "⏱ Foydalanuvchi captchani yechmadi va guruhdan chiqarildi."
            )
        except Exception as e:
            logger.error(f"Captcha timeout kick xatoligi: {e}")


# =============================================
#  YANGI A'ZO — yagona handler
#  (anti-bot + captcha + welcome)
# =============================================

@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def on_new_member(message: types.Message):
    """
    Yangi a'zo qo'shilganda ishlaydi.
    Tartib: anti-bot → captcha → welcome xabari.
    """
    settings = await get_group_settings(message.chat.id)

    for new_member in message.new_chat_members:
        # --- 1. ANTI-BOT: bot qo'shilsa, chiqarish ---
        if new_member.is_bot:
            if settings["anti_bot"]:
                # Admin qo'shgan bo'lsa, ruxsat beramiz
                try:
                    adder = await message.chat.get_member(message.from_user.id)
                    if adder.is_chat_admin():
                        continue  # Admin qo'shgan — ruxsat
                except Exception:
                    pass

                try:
                    await message.chat.kick(user_id=new_member.id)
                    await log_action(
                        chat_id=message.chat.id, action="auto_kick_bot",
                        user_id=new_member.id, user_name=new_member.full_name,
                        admin_id=message.from_user.id, admin_name=message.from_user.full_name,
                    )
                    await message.answer(
                        f"🤖 Bot <b>{new_member.full_name}</b> chiqarildi.\n"
                        f"Faqat adminlar guruhga bot qo'sha oladi!"
                    )
                except Exception as e:
                    logger.error(f"Anti-bot xatoligi: {e}")
            continue  # Bot uchun welcome/captcha kerak emas

        # --- 2. CAPTCHA: foydalanuvchini tekshirish ---
        if settings["captcha_enabled"]:
            try:
                await message.chat.restrict(
                    user_id=new_member.id,
                    can_send_messages=False,
                )
            except Exception:
                pass

            question, answer = _generate_captcha()
            keyboard = _create_captcha_keyboard(answer)
            captcha_msg = await message.answer(
                f"👋 Salom, {new_member.get_mention(as_html=True)}!\n\n"
                f"🔢 Guruhga kirish uchun misolni yeching:\n"
                f"<b>{question} = ?</b>\n\n"
                f"⏱ Vaqt: 60 soniya",
                reply_markup=keyboard,
            )
            _pending_captcha[(message.chat.id, new_member.id)] = {
                "answer": answer,
                "msg_id": captcha_msg.message_id,
            }
            asyncio.create_task(_captcha_timeout(message.chat.id, new_member.id, 60))
            continue  # Captcha bor, welcome keyin (to'g'ri javob berganda)

        # --- 3. WELCOME: xush kelibsiz xabari ---
        welcome = settings.get("welcome_text")
        if welcome:
            text = welcome.replace(
                "{name}", new_member.get_mention(as_html=True)
            ).replace(
                "{group}", message.chat.title or "guruh"
            )
        else:
            text = f"👋 Xush kelibsiz, {new_member.get_mention(as_html=True)}!"

        welcome_msg = await message.reply(text)

        if settings["auto_delete_joins"]:
            asyncio.create_task(auto_clean(message, welcome_msg, delay=30))


# =============================================
#  CAPTCHA CALLBACK
# =============================================

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("captcha:"))
async def captcha_callback(callback: types.CallbackQuery):
    """Captcha tugmasi bosilganda javobni tekshiradi."""
    key = (callback.message.chat.id, callback.from_user.id)

    if key not in _pending_captcha:
        await callback.answer("Bu captcha siz uchun emas!", show_alert=True)
        return

    selected = int(callback.data.split(":")[1])
    expected = _pending_captcha[key]["answer"]

    if selected == expected:
        del _pending_captcha[key]

        # Cheklovlarni olib tashlash
        try:
            user_permissions = types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
            )
            await callback.message.chat.restrict(
                user_id=callback.from_user.id,
                permissions=user_permissions,
                until_date=0,
            )
        except Exception:
            pass

        # Welcome xabari
        settings = await get_group_settings(callback.message.chat.id)
        welcome = settings.get("welcome_text")
        if welcome:
            welcome_text = welcome.replace(
                "{name}", callback.from_user.get_mention(as_html=True)
            ).replace(
                "{group}", callback.message.chat.title or "guruh"
            )
        else:
            welcome_text = f"✅ Xush kelibsiz, {callback.from_user.get_mention(as_html=True)}!"

        await callback.message.edit_text(welcome_text)
        await callback.answer("✅ To'g'ri! Xush kelibsiz!")
    else:
        await callback.answer("❌ Noto'g'ri javob! Qayta urinib ko'ring.", show_alert=True)


# =============================================
#  A'ZO TARK ETGANDA
# =============================================

@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def on_member_left(message: types.Message):
    """A'zo guruhni tark etganda yoki haydalganda xabar yuboradi."""
    settings = await get_group_settings(message.chat.id)
    left = message.left_chat_member
    bot_id = (await bot.me).id

    if message.from_user.id == bot_id:
        return

    if left.id == message.from_user.id:
        leave_msg = await message.answer(
            f"👤 {left.get_mention(as_html=True)} guruhni tark etdi."
        )
    else:
        leave_msg = await message.answer(
            f"🔨 {left.full_name} guruhdan haydaldi.\n"
            f"👮 Admin: {message.from_user.get_mention(as_html=True)}"
        )

    if settings["auto_delete_joins"]:
        asyncio.create_task(auto_clean(message, leave_msg, delay=30))


# =============================================
#  WELCOME BOSHQARUVI
# =============================================

@dp.message_handler(IsGroup(), Command("setwelcome", prefixes="!/"), AdminFilter())
async def set_welcome_text(message: types.Message):
    """
    Xush kelibsiz xabarini sozlash.
    Ishlatilishi: /setwelcome Salom, {name}! {group} guruhiga xush kelibsiz!
    """
    text = message.get_args()
    if not text:
        await message.reply(
            "⚠️ Ishlatilishi:\n"
            "/setwelcome Salom, {name}! {group} guruhiga xush kelibsiz!\n\n"
            "O'zgaruvchilar:\n"
            "  {name} — yangi a'zo ismi\n"
            "  {group} — guruh nomi\n\n"
            "O'chirish: /resetwelcome"
        )
        return

    await update_group_setting(message.chat.id, "welcome_text", text)
    await message.reply(f"✅ Xush kelibsiz xabari sozlandi:\n\n<i>{text}</i>")


@dp.message_handler(IsGroup(), Command("resetwelcome", prefixes="!/"), AdminFilter())
async def reset_welcome_text(message: types.Message):
    """Xush kelibsiz xabarini standart holatga qaytarish."""
    await update_group_setting(message.chat.id, "welcome_text", None)
    await message.reply("✅ Xush kelibsiz xabari standart holatga qaytarildi.")