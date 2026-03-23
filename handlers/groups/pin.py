"""
Pin/Unpin va Mute/Unmute buyruqlari.
"""
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
#  PIN — Xabarni pin qilish
# =============================================

@dp.message_handler(IsGroup(), Command("pin", prefixes="!/"), AdminFilter())
async def pin_message(message: types.Message):
    """Reply qilingan xabarni pin qiladi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Pin qilish uchun xabarga reply qiling!")
        return

    try:
        await reply.pin()
        await log_action(
            chat_id=message.chat.id, action="pin",
            admin_id=message.from_user.id, admin_name=message.from_user.full_name,
        )
        result_msg = await message.answer("📌 Xabar pin qilindi!")
        asyncio.create_task(auto_clean(message, result_msg))
    except Exception as err:
        await message.reply(f"❌ Xatolik: {err}")


@dp.message_handler(IsGroup(), Command("unpin", prefixes="!/"), AdminFilter())
async def unpin_message(message: types.Message):
    """Oxirgi pinni olib tashlaydi."""
    try:
        await bot.unpin_chat_message(message.chat.id)
        await log_action(
            chat_id=message.chat.id, action="unpin",
            admin_id=message.from_user.id, admin_name=message.from_user.full_name,
        )
        result_msg = await message.answer("📌 Pin olib tashlandi!")
        asyncio.create_task(auto_clean(message, result_msg))
    except Exception as err:
        await message.reply(f"❌ Xatolik: {err}")


# =============================================
#  MUTE — Ovozli/media cheklash
# =============================================

@dp.message_handler(IsGroup(), Command("mute", prefixes="!/"), AdminFilter())
async def mute_user(message: types.Message):
    """
    Foydalanuvchini mute qiladi (media, stiker, GIF yuborish taqiqlanadi).
    /ro dan farqi: /mute da matn yozish mumkin, faqat media taqiqlanadi.
    Ishlatilishi: /mute [daqiqa]
    """
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user
    args = message.get_args()
    time_minutes = int(args) if args and args.isdigit() else 30

    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time_minutes)

    mute_permissions = types.ChatPermissions(
        can_send_messages=True,           # Matn yozish mumkin
        can_send_media_messages=False,    # Media taqiq
        can_send_polls=False,             # So'rovnomalar taqiq
        can_send_other_messages=False,    # Stiker, GIF taqiq
        can_add_web_page_previews=False,  # Havola preview taqiq
        can_invite_users=False,
        can_change_info=False,
        can_pin_messages=False,
    )

    try:
        await message.chat.restrict(
            user_id=member.id,
            permissions=mute_permissions,
            until_date=until_date,
        )
        await log_action(
            chat_id=message.chat.id, action="mute",
            user_id=member.id, user_name=member.full_name,
            admin_id=message.from_user.id, admin_name=message.from_user.full_name,
            reason=f"{time_minutes} daqiqa",
        )
        result_msg = await message.answer(
            f"🔇 <b>{member.full_name}</b> {time_minutes} daqiqa mute qilindi.\n"
            f"📝 Matn yozish mumkin, media taqiqlangan."
        )
        asyncio.create_task(auto_clean(message, result_msg))
    except Exception as err:
        await message.reply(f"❌ Xatolik: {err}")


@dp.message_handler(IsGroup(), Command("unmute", prefixes="!/"), AdminFilter())
async def unmute_user(message: types.Message):
    """Foydalanuvchini mute'dan chiqaradi."""
    reply = message.reply_to_message
    if not reply:
        await message.reply("⚠️ Bu buyruqni ishlatish uchun foydalanuvchi xabariga reply qiling!")
        return

    member = reply.from_user

    full_permissions = types.ChatPermissions(
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
            permissions=full_permissions,
            until_date=0,
        )
        await log_action(
            chat_id=message.chat.id, action="unmute",
            user_id=member.id, user_name=member.full_name,
            admin_id=message.from_user.id, admin_name=message.from_user.full_name,
        )
        result_msg = await message.answer(
            f"🔊 <b>{member.full_name}</b> mute'dan chiqarildi."
        )
        asyncio.create_task(auto_clean(message, result_msg))
    except Exception as err:
        await message.reply(f"❌ Xatolik: {err}")
