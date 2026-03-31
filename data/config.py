"""
Loyihani konfiguratsiya sozlash.
Environment variables (.env faylidan) o'qiydi.
"""
import os
from pathlib import Path
from environs import Env

# Environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# ╔════════════════════════════════════════════╗
# ║   TELEGRAM BOT SOZLAMALARI                 ║
# ╚════════════════════════════════════════════╝

# Bot token (@BotFather dan oling)
BOT_TOKEN = env.str("BOT_TOKEN")

# Adminlarning ID'lari (vergul bilan ajratilgan)
ADMINS = env.list("ADMINS", cast=int)

# Xostning IP manzili (webhook uchun)
IP = env.str("ip", default="localhost")

# ╔════════════════════════════════════════════╗
# ║   DATABASE SOZLAMALARI                     ║
# ╚════════════════════════════════════════════╝

# Database fayli joylashuvi
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = env.str("DATABASE_URL", default=str(BASE_DIR / "data" / "bot.db"))

# ╔════════════════════════════════════════════╗
# ║   LOGGING SOZLAMALARI                      ║
# ╚════════════════════════════════════════════╝

# Log fayllari joylashuvi
LOGS_DIR = env.str("LOGS_DIR", default=str(BASE_DIR / "logs"))

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "bot.log")
LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")

# ╔════════════════════════════════════════════╗
# ║   BOT XUSUSIYATLARI SOZLAMALARI           ║
# ╚════════════════════════════════════════════╝

# Default ogohlantirshlar soni
DEFAULT_WARNS = env.int("DEFAULT_WARNS", default=3)

# Default flood limit (xabarlar soni)
DEFAULT_FLOOD_LIMIT = env.int("DEFAULT_FLOOD_LIMIT", default=5)

# Default flood vaqti (soniyalarda)
DEFAULT_FLOOD_TIME = env.int("DEFAULT_FLOOD_TIME", default=10)

# ╔════════════════════════════════════════════╗
# ║   VALIDATION (TEKSHIRUV)                   ║
# ╚════════════════════════════════════════════╝

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylida to'g'ri sozlanmagan!")

if not ADMINS:
    raise ValueError("❌ ADMINS .env faylida bo'sh!")

if len(ADMINS) == 0:
    raise ValueError("❌ ADMINS ro'yxatida hech kim yo'q!")

