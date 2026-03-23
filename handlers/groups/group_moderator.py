import asyncio
import datetime
import logging

from aiogram import types
from aiogram.dispatcher.filters import Command

from core.filters import IsGroup, AdminFilter
from core.database.models import log_action
from core.utils.message_manager import auto_clean
from loader import dp, bot

logger = logging.getLogger(__name__)

# =============================================
#  READ ONLY (RO) — Yozish huquqini cheklash
# =============================================

@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"), AdminFilter())
async def read_only_mode(message: types.Message):
    """
    Foydalanuvchini vaqtincha Read-Only rejimga o'tkazadi.
    Ishlatilishi:
        !ro          — 5 daqiqaga cheklash (standart)
        !ro 30       — 30 daqiqaga cheklash
        !ro 10 spam  — 10 daqiqaga, sabab: spam
    """
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user

    # Buyruq argumentlarini tahlil qilish
    args = message.get_args()
    parts = args.split(maxsplit=1) if args else []

    # Vaqtni aniqlash (standart: 5 daqiqa)
    time_minutes = 5
    comment = None

    if parts:
        if parts[0].isdigit():
            time_minutes = int(parts[0])
            comment = parts[1] if len(parts) > 1 else None
        else:
            comment = args

    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time_minutes)

    try:
        await message.chat.restrict(
            user_id=member.id,
            can_send_messages=False,
            until_date=until_date,
        )
        await reply.delete()
    except Exception as err:
        logger.error(f"RO buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")
        return

    # Log yozish
    await log_action(
        chat_id=message.chat.id, action="ro",
        user_id=member.id, user_name=member.full_name,
        admin_id=message.from_user.id, admin_name=message.from_user.full_name,
        reason=comment or f"{time_minutes} daqiqa",
    )

    # Natija haqida xabar
    text = f"🔇 <b>{member.full_name}</b> {time_minutes} daqiqa yozish huquqidan mahrum qilindi."
    if comment:
        text += f"\n📝 Sabab: <b>{comment}</b>"

    result_msg = await message.answer(text)
    asyncio.create_task(auto_clean(message, result_msg))


# =============================================
#  UNRO — Read-Only holatdan tiklash
# =============================================

@dp.message_handler(IsGroup(), Command("unro", prefixes="!/"), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    """Foydalanuvchini Read-Only holatdan chiqaradi va huquqlarini tiklaydi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user

    user_permissions = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )

    try:
        await message.chat.restrict(
            user_id=member.id,
            permissions=user_permissions,
            until_date=0,
        )
    except Exception as err:
        logger.error(f"UNRO buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")
        return

    await log_action(
        chat_id=message.chat.id, action="unro",
        user_id=member.id, user_name=member.full_name,
        admin_id=message.from_user.id, admin_name=message.from_user.full_name,
    )

    result_msg = await message.answer(f"🔊 <b>{member.full_name}</b> tiklandi va yozish huquqi qaytarildi.")
    asyncio.create_task(auto_clean(message, result_msg))


# =============================================
#  BAN — Guruhdan haydash
# =============================================

@dp.message_handler(IsGroup(), Command("ban", prefixes="!/"), AdminFilter())
async def ban_user(message: types.Message):
    """Foydalanuvchini guruhdan butunlay haydaydi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user

    try:
        await message.chat.kick(user_id=member.id)
    except Exception as err:
        logger.error(f"BAN buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")
        return

    await log_action(
        chat_id=message.chat.id, action="ban",
        user_id=member.id, user_name=member.full_name,
        admin_id=message.from_user.id, admin_name=message.from_user.full_name,
    )

    result_msg = await message.answer(f"🔨 <b>{member.full_name}</b> guruhdan haydaldi.")
    asyncio.create_task(auto_clean(message, result_msg))


# =============================================
#  UNBAN — Bandan chiqarish
# =============================================

@dp.message_handler(IsGroup(), Command("unban", prefixes="!/"), AdminFilter())
async def unban_user(message: types.Message):
    """Foydalanuvchini bandan chiqaradi (o'zi qayta qo'shilishi mumkin)."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user

    try:
        await message.chat.unban(user_id=member.id)
    except Exception as err:
        logger.error(f"UNBAN buyrug'ida xatolik: {err}")
        await message.answer(f"❌ Xatolik: {err}")
        return

    await log_action(
        chat_id=message.chat.id, action="unban",
        user_id=member.id, user_name=member.full_name,
        admin_id=message.from_user.id, admin_name=message.from_user.full_name,
    )

    result_msg = await message.answer(f"🕊 <b>{member.full_name}</b> bandan chiqarildi.")
    asyncio.create_task(auto_clean(message, result_msg))
