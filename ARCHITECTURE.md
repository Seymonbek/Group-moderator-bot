# 🏗️ Texnik Arxitektura

## 📐 Tizim Arxitekturasi

```
┌─────────────────────────────────────────────────────────┐
│                   Users & Admins                        │
│              Telegram Mobile App / Web                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Polling/Webhook
                     │
┌────────────────────▼────────────────────────────────────┐
│              Telegram Bot API                           │
│         (via aiogram library)                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Dispatcher / FSM Storage                      │
│    (Routes messages & manages user states)             │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐  ┌───▼────┐  ┌──▼───────┐
    │ Filters │  │Handlers│  │Middleware│
    └────┬────┘  └───┬────┘  └──┬───────┘
         │           │          │
         └───────────┼──────────┘
                     │
         ┌───────────┼──────────────┐
         │           │              │
    ┌────▼─────┐  ┌──▼────────┐ ┌──▼─────┐
    │ Database │  │  Locales  │ │ Utils  │
    │ (SQLite) │  │ (i18n)    │ │ (Logs) │
    └──────────┘  └───────────┘ └────────┘
```

## 🔄 Request Jarayoni

```
1. User Telegram'da xabar yuboradi
                │
                ▼
2. Bot API orqali Dispatcher'ga keladi
                │
                ▼
3. Middleware'lar tekshiradi (throttling, stats)
                │
                ▼
4. Filtrlar qo'llaniladi (admin, chat_type)
                │
                ▼
5. Handler tanlanadi (va jarayoni aniqlanadi)
                │
                ▼
6. Command yoki message tekshiriladi
                │
                ▼
7. Database'ga murojaat qilish (agar kerak bo'lsa)
                │
                ▼
8. Javob tayyorlanadi (lokalizatsiya bilan)
                │
                ▼
9. User'ga javob yuboriladi
```

## 📦 Component Details

### 1. **Loader** (`loader.py`)
- Bot va Dispatcher'ni ishga tushiradi
- MemoryStorage'ni sozlaydi (state management uchun)

```python
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
```

### 2. **Filters** (`core/filters/`)

#### Admin Filter
```python
# Admin buyruqlari uchun
@dp.message_handler(is_admin=True, commands=['ban'])
async def ban_user(message: Message):
    pass
```

#### Chat Type Filter
```python
# Faqat gruppada ishlaydi
@dp.message_handler(chat_type=['supergroup', 'group'])
async def group_message(message: Message):
    pass
```

### 3. **Middlewares** (`core/middlewares/`)

#### Throttling Middleware
- Spam xabarlarni aniqlaydi
- Rate limiting qo'yadi

#### Anti-Flood Middleware
- Vaqt ichida ko'p xabar jo'natilishini tekshiradi
- Parametrlari: `flood_limit`, `flood_time`

#### Stats Counter Middleware
- Barcha xabarlarni statistika uchun hisoblab turadi

### 4. **Database** (`core/database/`)

#### Connection Pool
```python
_db: aiosqlite.Connection | None = None

async def get_db() -> aiosqlite.Connection:
    global _db
    if _db is None:
        _db = await aiosqlite.connect(DB_PATH)
        _db.row_factory = aiosqlite.Row
    return _db
```

#### Schema
- **groups**: Guruh sozlamalari
- **warns**: Ogohlantirshlar
- **stats**: Statistika
- **users**: Foydalanuvchi ma'lumotlari

### 5. **Handlers** (`handlers/`)

```
handlers/
├── errors/
│   └── error_handler.py       # Global xato ushlash
├── groups/
│   ├── auto_moderation.py     # Avtomatik moderatsiya
│   ├── group_moderator.py     # Moderator buyruqlari
│   ├── warn.py                # Warn sistema
│   ├── settings.py            # Guruh sozlamalari
│   └── ...
└── users/
    ├── start.py               # /start buyrugi
    ├── help.py                # /help buyrugi
    └── ...
```

### 6. **Locales** (`core/locales/`)

Multi-language support:
```python
locales = {
    'uz': {...},
    'ru': {...},
    'en': {...}
}
```

## 🗄️ Database Schema

### Groups Table
```sql
CREATE TABLE groups (
    chat_id INTEGER PRIMARY KEY,
    anti_link INTEGER DEFAULT 0,
    anti_flood INTEGER DEFAULT 0,
    anti_bot INTEGER DEFAULT 0,
    anti_forward INTEGER DEFAULT 0,
    anti_arabic INTEGER DEFAULT 0,
    anti_emoji_spam INTEGER DEFAULT 0,
    bad_words_enabled INTEGER DEFAULT 0,
    captcha_enabled INTEGER DEFAULT 0,
    auto_delete_joins INTEGER DEFAULT 0,
    welcome_text TEXT DEFAULT NULL,
    log_channel_id INTEGER DEFAULT NULL,
    language TEXT DEFAULT 'uz',
    max_warns INTEGER DEFAULT 3,
    flood_limit INTEGER DEFAULT 5,
    flood_time INTEGER DEFAULT 10
);
```

### Warns Table
```sql
CREATE TABLE warns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_name TEXT,
    reason TEXT,
    admin_id INTEGER,
    admin_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES groups(chat_id)
);
```

## 🔐 Xavfsizlik Arxitekturasi

```
┌──────────────────────────────────────┐
│       Telegram Bot API               │
│  (OAuth, TLS encryption)             │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│    Admin Authentication               │
│    (Telegram User ID verification)   │
└──────────────────┬───────────────────┘
                   │
            ┌──────┴──────┐
            ▼             ▼
      ┌──────────┐  ┌────────────┐
      │ Allowed  │  │ Forbidden  │
      │ Commands │  │ Response   │
      └──────────┘  └────────────┘
```

## 📊 State Management (FSM)

```python
class UserStates(StatesGroup):
    waiting_for_reason = State()
    waiting_for_confirm = State()
```

MemoryStorage'da saqlanadi (default), production'da Redis tavsiya etiladi.

## 🔄 Event Flow

### Spam Xabar Tekshiruvi

```
1. Message keladi
   │
2. Anti-Flood tekshiruvi
   ├─ Vaqt ichida xabar soni > flood_limit?
   │  ├─ Yo: User mute qilindi
   │  └─ Yoq: Davom
   │
3. Anti-Link tekshiruvi
   ├─ Link mavjud?
   │  ├─ Yo: Anti-link xususiyati yoqilgan?
   │  │  ├─ Yo: Xabar o'chirildi
   │  │  └─ Yoq: Davom
   │  └─ Yoq: Davom
   │
4. Bad Words filtri
   ├─ Zburish so'z tavari?
   │  ├─ Yo: O'chirildi
   │  └─ Yoq: Davom
   │
5. Xabar saqlanadi (stats uchun)
```

## ⚡ Performance Optimization

### Database
- **WAL Mode**: Write-Ahead Logging
- **Foreign Keys**: Enabled
- **Row Factory**: Automatic dict conversion

### Caching
```python
# Modulda keshlanadi
group_settings_cache = {}

async def get_group_settings(chat_id: int):
    if chat_id not in group_settings_cache:
        # Database'dan olinadi
        settings = await db.fetch(...)
        group_settings_cache[chat_id] = settings
    return group_settings_cache[chat_id]
```

### Async Operations
Barcha I/O operatsiyalar asinxron:
```python
async def handle_message(message: Message):
    await message.delete()           # Non-blocking
    await send_log(message)          # Non-blocking
    await update_database(message)   # Non-blocking
```

## 🔍 Monitoring & Logging

### Log Levels
```
DEBUG   - Detailed information for debugging
INFO    - General information
WARNING - Warning messages
ERROR   - Error messages
CRITICAL- Critical issues
```

### Log Format
```
%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s
```

**Example:**
```
app.py [LINE:45] #ERROR [2024-03-31 10:30:45] Bot token is invalid
```

## 🚀 Scalability

### Current Limitations
- MemoryStorage: Server qayta ishga tushganda session lost
- SQLite: Bir nechta process'dan muammo bo'lishi mumkin
- Single instance

### Scaling Solutions
1. **Session Storage**: Redis
2. **Database**: PostgreSQL
3. **Multiple Instances**: Kubernetes/Docker Compose
4. **Message Queue**: Celery/RabbitMQ

## 📝 Code Organization

```
app.py          ─ Entry point
loader.py       ─ Bot initialization
data/
├── config.py   ─ Configuration
└── bot.db      ─ SQLite database
core/
├── database/   ─ Database operations
├── filters/    ─ Custom filters
├── middlewares/─ Middleware processors
├── locales/    ─ i18n translations
└── utils/      ─ Helper functions
handlers/
├── errors/     ─ Error handling
├── groups/     ─ Group operations
└── users/      ─ User operations
```

## 🔄 Dependency Injection Pattern

```python
# Loader'da yaratiladi
bot = Bot(...)
dp = Dispatcher(...)

# Handlers'da ishlatiladi
async def handler(message: Message):
    # message object injected by dispatcher
    pass
```

---

Bu arxitektura production-ready va test-friendly tayyorlangandir.
