import asyncio
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from core.filters import IsGroup, AdminFilter
from core.database.models import (
    add_warn, get_warn_count, get_warns,
    remove_last_warn, reset_warns, get_group_settings, log_action,
)
from core.utils.message_manager import auto_clean
from loader import dp, bot

logger = logging.getLogger(__name__)


# =============================================
#  WARN — Ogohlantirish berish
# =============================================

@dp.message_handler(IsGroup(), Command("warn", prefixes="!/"), AdminFilter())
async def warn_user(message: types.Message):
    """
    Foydalanuvchiga ogohlantirish beradi.
    3 ta warn = avtomatik ban (sozlamaga qarab).
    Ishlatilishi: /warn [sabab]
    """
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user

    # Adminni warn qilishga ruxsat yo'q
    chat_member = await message.chat.get_member(member.id)
    if chat_member.is_chat_admin():
        await message.reply("❌ Adminga ogohlantirish berish mumkin emas!")
        return

    # Sababni olish
    reason = message.get_args() or "Sabab ko'rsatilmagan"

    # Bazaga yozish
    settings = await get_group_settings(message.chat.id)
    max_warns = settings["max_warns"]

    warn_count = await add_warn(
        chat_id=message.chat.id,
        user_id=member.id,
        user_name=member.full_name,
        reason=reason,
        admin_id=message.from_user.id,
        admin_name=message.from_user.full_name,
    )

    # Log yozish
    await log_action(
        chat_id=message.chat.id,
        action="warn",
        user_id=member.id,
        user_name=member.full_name,
        admin_id=message.from_user.id,
        admin_name=message.from_user.full_name,
        reason=reason,
    )

    if warn_count >= max_warns:
        # Avtomatik ban
        try:
            await message.chat.kick(user_id=member.id)
            await reset_warns(message.chat.id, member.id)
            await log_action(
                chat_id=message.chat.id,
                action="auto_ban",
                user_id=member.id,
                user_name=member.full_name,
                admin_id=message.from_user.id,
                admin_name=message.from_user.full_name,
                reason=f"{max_warns} ta ogohlantirish to'plandi",
            )
            result_msg = await message.answer(
                f"🔨 <b>{member.full_name}</b> guruhdan haydaldi!\n"
                f"📝 Sabab: {max_warns} ta ogohlantirish to'plandi."
            )
        except Exception as err:
            logger.error(f"Auto-ban xatoligi: {err}")
            result_msg = await message.answer(f"❌ Avtomatik ban qilishda xatolik: {err}")
    else:
        result_msg = await message.answer(
            f"⚠️ <b>{member.full_name}</b> ga ogohlantirish berildi!\n"
            f"📝 Sabab: <b>{reason}</b>\n"
            f"📊 Ogohlantirshlar: <b>{warn_count}/{max_warns}</b>"
        )

    asyncio.create_task(auto_clean(message, result_msg))


# =============================================
#  UNWARN — Oxirgi ogohlantirshni olish
# =============================================

@dp.message_handler(IsGroup(), Command("unwarn", prefixes="!/"), AdminFilter())
async def unwarn_user(message: types.Message):
    """Foydalanuvchining oxirgi ogohlantirshini olib tashlaydi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user
    removed = await remove_last_warn(message.chat.id, member.id)

    if removed:
        remaining = await get_warn_count(message.chat.id, member.id)
        settings = await get_group_settings(message.chat.id)
        result_msg = await message.answer(
            f"✅ <b>{member.full_name}</b> ning oxirgi ogohlantirishsi olib tashlandi.\n"
            f"📊 Qolgan: <b>{remaining}/{settings['max_warns']}</b>"
        )
    else:
        result_msg = await message.answer(
            f"ℹ️ <b>{member.full_name}</b> ning ogohlantirishlari yo'q."
        )

    asyncio.create_task(auto_clean(message, result_msg))


# =============================================
#  WARNS — Ogohlantirshlar ro'yxati
# =============================================

@dp.message_handler(IsGroup(), Command("warns", prefixes="!/"), AdminFilter())
async def list_warns(message: types.Message):
    """Foydalanuvchining barcha ogohlantirshlarini ko'rsatadi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user
    warns = await get_warns(message.chat.id, member.id)
    settings = await get_group_settings(message.chat.id)

    if not warns:
        await message.answer(f"✅ <b>{member.full_name}</b> ning ogohlantirishlari yo'q.")
        return

    text = f"⚠️ <b>{member.full_name}</b> ning ogohlantirishlari ({len(warns)}/{settings['max_warns']}):\n\n"
    for i, warn in enumerate(warns, 1):
        reason = warn['reason'] if warn['reason'] else "Sabab ko'rsatilmagan"
        text += f"  {i}. {reason}\n"
        text += f"     👮 {warn['admin_name']} | 📅 {warn['created_at'][:16]}\n"

    await message.answer(text)


# =============================================
#  RESETWARNS — Barcha ogohlantirshlarni tozalash
# =============================================

@dp.message_handler(IsGroup(), Command("resetwarns", prefixes="!/"), AdminFilter())
async def reset_user_warns(message: types.Message):
    """Foydalanuvchining barcha ogohlantirshlarini tozalaydi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user
    count = await reset_warns(message.chat.id, member.id)

    if count > 0:
        result_msg = await message.answer(
            f"🧹 <b>{member.full_name}</b> ning {count} ta ogohlantirishsi tozalandi."
        )
    else:
        result_msg = await message.answer(
            f"ℹ️ <b>{member.full_name}</b> ning ogohlantirishlari yo'q."
        )

    asyncio.create_task(auto_clean(message, result_msg))
