from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    """Bot uchun standart buyruqlar ro'yxatini o'rnatadi."""
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Botni ishga tushirish"),
        types.BotCommand("help", "Yordam — barcha buyruqlar ro'yxati"),
        types.BotCommand("settings", "Sozlamalar paneli"),
        types.BotCommand("stats", "Guruh statistikasi"),
        types.BotCommand("ro", "Read Only rejimga o'tkazish"),
        types.BotCommand("unro", "Read Only rejimdan chiqarish"),
        types.BotCommand("ban", "Guruhdan haydash"),
        types.BotCommand("unban", "Bandan chiqarish"),
        types.BotCommand("mute", "Media yuborishni cheklash"),
        types.BotCommand("unmute", "Mute'dan chiqarish"),
        types.BotCommand("warn", "Ogohlantirish berish"),
        types.BotCommand("unwarn", "Ogohlantirshni olish"),
        types.BotCommand("warns", "Ogohlantirshlar ro'yxati"),
        types.BotCommand("pin", "Xabarni pin qilish"),
        types.BotCommand("unpin", "Pinni olib tashlash"),
        types.BotCommand("set_photo", "Guruh rasmini o'zgartirish"),
        types.BotCommand("set_title", "Guruh nomini o'zgartirish"),
        types.BotCommand("set_description", "Guruh tavsifini o'zgartirish"),
    ])
