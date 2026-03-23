from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


HELP_TEXT = """
📋 <b>Buyruqlar ro'yxati:</b>

<b>━━━ Umumiy ━━━</b>
/start — Botni ishga tushirish
/help — Ushbu yordam xabari

<b>━━━ Moderatsiya (adminlar uchun) ━━━</b>
/ro <i>[daqiqa] [sabab]</i> — Read Only rejimga o'tkazish
/unro — Read Only rejimdan chiqarish
/ban — Guruhdan haydash
/unban — Bandan chiqarish
/mute <i>[daqiqa]</i> — Media yuborishni cheklash
/unmute — Mute'dan chiqarish
/pin — Xabarni pin qilish
/unpin — Pinni olib tashlash

<b>━━━ Ogohlantirish tizimi ━━━</b>
/warn <i>[sabab]</i> — Ogohlantirish berish (3 warn = ban)
/unwarn — Oxirgi ogohlantirshni olish
/warns — Ogohlantirshlar ro'yxati
/resetwarns — Barcha ogohlantirshlarni tozalash

<b>━━━ Guruh sozlamalari ━━━</b>
/set_photo — Guruh rasmini o'zgartirish
/set_title — Guruh nomini o'zgartirish
/set_description — Guruh tavsifini o'zgartirish
/setwelcome <i>[matn]</i> — Xush kelibsiz xabarini sozlash
/resetwelcome — Standart welcome'ga qaytarish

<b>━━━ So'z filtri ━━━</b>
/addword <i>[so'z]</i> — Taqiqlangan so'z qo'shish
/delword <i>[so'z]</i> — Taqiqlangan so'zni o'chirish
/badwords — Taqiqlangan so'zlar ro'yxati

<b>━━━ Boshqaruv ━━━</b>
/settings — Sozlamalar paneli (inline tugmalar)
/stats — Guruh statistikasi
/setlog <i>[kanal_id]</i> — Log kanalini sozlash
/unsetlog — Log kanalini o'chirish

<b>━━━ Avtomatik himoya ━━━</b>
🔗 Anti-link | 🌊 Anti-flood | 🤖 Anti-bot
🔄 Anti-forward | 🔤 Anti-arabic | 😀 Anti-emoji
🤬 So'z filtri | 🔢 Captcha | 🧹 Auto-delete

💡 <i>Barchasi /settings orqali on/off qilinadi!</i>
💡 <i>Moderatsiya buyruqlari uchun xabarga reply qiling!</i>
""".strip()


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    """Barcha mavjud buyruqlar haqida ma'lumot beradi."""
    await message.answer(HELP_TEXT)