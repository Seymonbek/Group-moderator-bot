# 👥 Groups Moderator Bot

Telegram guruhlarini avtomatik ravishda moderatsiya qiluvchi bot. Spamni, linkni, arabcha va boshqa noxush kontentni blokirovka qiladi.

**Languages**: [O'zbek](#-o'zbek) | [English](#-english)

---

## 🇺🇿 O'zbek

### ✨ Xususiyatlari

- ✅ **Anti-Spam**: Spam xabarlarini aniqlaydi va o'chiradi
- ✅ **Anti-Link**: Talmasiz linklar blokirovka qiladi
- ✅ **Anti-Bot**: Botlarni guruhdan olib tashlaydi
- ✅ **Anti-Forward**: Forwarded xabarlarni blokirovka qiladi
- ✅ **Anti-Arabic**: Arabcha yozuvlarni filtrlaydi
- ✅ **Anti-Emoji Spam**: Emoji-spam o'chiriladi
- ✅ **Bad Words Filter**: Zburish so'zlarini aniqlaydi
- ✅ **CAPTCHA**: Yeni a'zolar uchun CAPTCHA tekshirish
- ✅ **Warn System**: Xabar berilgan foydalanuvchilar ta'minlanadi
- ✅ **Avto-Delete Joins**: Kirish/chiqish xabarlarini avtomatik o'chiradi
- ✅ **Log Channel**: Barcha voqealarni log-channelga yozadi
- ✅ **Multi-language**: Uz, Ru, En tillarida qo'llab-quvvatlash

### 📋 Talablar

- Python 3.8+
- pip (Python paket menejeri)
- SQLite3 (odatiy o'rnatilgan)

### 🚀 Instolatsiya

#### 1. Repositoriyani klonlash

```bash
git clone https://github.com/yourusername/groups-moderator-bot.git
cd groups-moderator-bot
```

#### 2. Virtual muhitni yaratish

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Dependensiyalarni o'rnatish

```bash
pip install -r requirements.txt
```

#### 4. .env faylini sozlash

`.env.dist` faylini `.env` ga kopiyalang va quyidagi ma'lumotlarni yozing:

```bash
cp .env.dist .env
```

`.env` faylini tahrirlang:

```env
ADMINS=123456789,987654321
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij
ip=localhost
```

**Ma'lumot:**
- `BOT_TOKEN`: [@BotFather](https://t.me/BotFather) dan oling
- `ADMINS`: Adminlarning Telegram ID'lari (vergul bilan ajratilgan)

#### 5. Botni ishga tushirish

```bash
python app.py
```

### 🔧 Konfiguratsiya

#### Guruh sozlamalari

Bot guruhga qoshnilganda, avtomatik ravishda standart sozlamalar bilan yangi yozuv yaratiladi.

**Yoqilshi mumkin bo'lgan xususiyatlar:**
```
/anti_link - Linklar blokirovka
/anti_flood - Flood blokirovka
/anti_bot - Botlar blokirovka
/anti_forward - Forward blokirovka
/anti_arabic - Arabcha blokirovka
/anti_emoji_spam - Emoji-spam blokirovka
/bad_words - Zburish so'zlar filtri
/captcha - CAPTCHA tekshiruvi
/auto_delete_joins - Avtomatik o'chirish
```

#### Ogohlantirsh (Warn) Tizimi

- Default: **3 ogohlantirsh** dan so'ng olib tashlash
- O'zgartirilishi mumkin `/max_warns` buyruq orqali

#### Flood Cheklovi

- Default: **5 xabar** har **10 soniyada**
- O'zgartirilishi mumkin `/flood_limit` va `/flood_time` orqali

### 📁 Loyiha Strukturasi

```
.
├── app.py                  # Bot asosiy faylი
├── loader.py              # Bot va Dispatcher sozlamasi
├── requirements.txt       # Python dependensiyalari
├── .env.dist              # Environment namunasi
├── data/
│   ├── config.py          # Konfiguratsiya
│   └── bot.db             # SQLite bazasi
├── core/
│   ├── database/          # Baza CRUD operatsiyalari
│   ├── filters/           # Avtoresmi filtrlar
│   ├── middlewares/       # Middleware'lar (anti-flood, stats)
│   ├── locales/           # Ko'p tillik qo'llab-quvvatlash
│   └── utils/             # Yordamchi funksiyalar
└── handlers/              # Buyruq handle'rlari
    ├── errors/
    ├── groups/            # Guruh moderatsiyasi
    └── users/             # Foydalanuvchi buyruqlari
```

### 📝 Asosiy Buyruqlar

**Foydalanuvchilar uchun:**
- `/start` - Botni ishga tushirish
- `/help` - Yordam

**Adminlar uchun:**
- `/settings` - Guruh sozlamalarini koʻrish/oʻzgartirish
- `/stats` - Statistika
- `/warn` - Foydalanuvchiga ogohlantirsh
- `/unwarn` - Ogohlantirshni bekor qilish
- `/ban` - Foydalanuvchini bannoga qoʻyish
- `/kick` - Foydalanuvchini olib tashlash
- `/mute` - Foydalanuvchini jimga qoʻyish

### 🗄️ Baza Strukturasi

#### `groups` Jadval
- `chat_id` - Guruh identifikatori
- `anti_link` - Linklar blokirovkasi (0/1)
- `anti_flood` - Flood blokirovkasi (0/1)
- `anti_bot` - Bot blokirovkasi (0/1)
- va hokazo...

#### `warns` Jadval
- `id` - Ogohlantirsh ID
- `chat_id`, `user_id` - Guruh va foydalanuvchi ID'lari
- `reason` - Ogohlantirsh sababi
- `admin_id`, `admin_name` - Admin ma'lumotlari

#### `stats` Jadval
- Xabarlar, rasmlar, video va boshqa ma'lumot statistikasi

### 🐛 Xato Tekshirish

Bot barcha xatolarni avtomatik ravishda ushlab tutadi va log qiladi:

```python
# Xavfsiz xatoliklar — loq qilinadi, lekin foydalanuvchiga ko'rsatilmaydi
# Kritik xatoliklar — admin'ga bildiriladi
```

**Log fayllari:** `logs/` direktoriyasida saqlanadi

### 📊 Monitoring

Botning ishlashini monitoring qilish uchun:

```bash
# Log qilgan xatorlarga qarang
tail -f logs/bot.log

# Bot jarayonini tekshirish
ps aux | grep python
```

### ⚙️ Deployment

#### Systemd Service (Linux)

1. Faylni yarating: `/etc/systemd/system/telegram-bot.service`

```ini
[Unit]
Description=Telegram Groups Moderator Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/bot
ExecStart=/path/to/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Servicedan foydalanish:

```bash
sudo systemctl start telegram-bot
sudo systemctl enable telegram-bot
sudo systemctl status telegram-bot
```

#### Docker (ixtiyoriy)

Dockerfile yarating:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]
```

### 🛡️ Xavfsizlik

- ⚠️ `.env` faylini hech qachon repositoriyaga push qilmang
- `.gitignore` ga `.env` qo'shing (allaqachon qo'shilgan)
- Bot tokenini hech qachon tagasiga bermang
- Admin ID'larini maxfiy saqlang

### 🔄 Development

```bash
# Dependensiyalarni yangilash
pip install -r requirements-dev.txt

# Kodni tuzatish
black core/ handlers/ data/
flake8 core/ handlers/ data/

# Unit testlar (agar mavjud bo'lsa)
pytest tests/
```

### 📞 Muammolarni Bildirich

Muammolar haqida bildirich uchun [Issues](https://github.com/yourusername/groups-moderator-bot/issues) yarating.

### 📄 Litsenziya

MIT License - [LICENSE](LICENSE) qarang.

### 👨‍💻 Hissa Qoʻshish

1. Repositoriyani fork qiling
2. Feature branch yarating (`git checkout -b feature/amazing`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add amazing feature'`)
4. Brunchga push qiling (`git push origin feature/amazing`)
5. Pull Request yarating

---

## 🇬🇧 English

### ✨ Features

- ✅ **Anti-Spam**: Detects and removes spam messages
- ✅ **Anti-Link**: Blocks unwanted links
- ✅ **Anti-Bot**: Removes bots from the group
- ✅ **Anti-Forward**: Blocks forwarded messages
- ✅ **Anti-Arabic**: Filters Arabic text
- ✅ **Anti-Emoji Spam**: Removes emoji spam
- ✅ **Bad Words Filter**: Detects profanity
- ✅ **CAPTCHA**: Verification for new members
- ✅ **Warn System**: Warns users before removal
- ✅ **Auto-Delete Joins**: Auto-removes join/leave messages
- ✅ **Log Channel**: Logs all events to a channel
- ✅ **Multi-language**: Support for Uz, Ru, En

### Requirements

- Python 3.8+
- pip (Python package manager)
- SQLite3 (usually pre-installed)

### 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/groups-moderator-bot.git
cd groups-moderator-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.dist .env
# Edit .env with your credentials

# Run the bot
python app.py
```

### 📋 Environment Variables

```env
ADMINS=123456789,987654321
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ip=localhost
```

### 🔧 Admin Commands

- `/start` - Start the bot
- `/help` - Get help
- `/settings` - View/change group settings
- `/warn [reason]` - Warn a user
- `/unwarn` - Remove warning
- `/ban` - Ban a user
- `/kick` - Kick a user
- `/mute` - Mute a user

### 🏗️ Project Structure

- `app.py` - Main bot entry point
- `loader.py` - Bot initialization
- `core/` - Core functionality (database, filters, middleware)
- `handlers/` - Command handlers
- `data/` - Configuration and database

### 🛡️ Security Notes

- **Never** commit `.env` to the repository
- Keep your bot token secret
- Admin IDs should be kept confidential

### 📞 Support

For issues and questions, please open an [Issue](https://github.com/yourusername/groups-moderator-bot/issues).

---

**Created with ❤️ by the Groups Moderator Bot team**
