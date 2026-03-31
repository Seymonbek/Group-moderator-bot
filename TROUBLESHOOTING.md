# 🐛 Qo'llab-Quvvatlash va Xato Tuzatish

## Umumiy Muammolar va Yechimlar

### **1. Bot ishga tushmaydi**

```
Error: Bot token is invalid
```

**Yechim:**
- Bot tokenini `@BotFather`dan qayta oling
- `.env` faylida `BOT_TOKEN` to'g'ri yozilganini tekshiring

```bash
# .env fayl tekshiruvi
grep "BOT_TOKEN" .env
```

---

### **2. Admin buyruqlari ishlama

**Sababi:** Sizning Telegram ID'ingiz `ADMINS` ro'yxatida yo'q

**Yechim:**
1. Sizning ID'ni bilib oling (@userinfobot ga yozing)
2. `.env` da qo'shding:
```env
ADMINS=your_id,other_admin_id
```

---

### **3. Ma'lumotlar bazasi xatosi**

```
sqlite3.OperationalError: database is locked
```

**Yechim:**
- Faqat bir bot jarayoni boshda bo'lsin
- Database daxli `PRAGMA journal_mode=WAL` ishlatiladi
- File permission'larni tekshiring

```bash
# Linux/Mac da
chmod 755 data/
```

---

### **4. Anti-flood ishlama

**Sababi:** Flood limit va vaqti noto'g'ri sozlangan

```python
# Default qiymatlar
flood_limit = 5      # Xabarlar soni
flood_time = 10      # Soniyalarda vaqt
```

**Yechim:** Admin buyruq orqali sozlang
```
/flood_limit 10
/flood_time 15
```

---

### **5. CAPTCHA ishlama

**Sababi:** Log channel sozlanmagan yoki permission'lar yo'q

**Yechim:**
1. Private channel yarating
2. Botni admin qiling
3. Channel ID'ni `log_channel_id` ga yazng:
```
/log_channel 123456789
```

---

## 📊 Monitoring va Debugging

### Loglarni Tekshirish

```bash
# Real-time monitoring
tail -f logs/bot.log

# Oxirgi 100 qatorni ko'rish
tail -100 logs/bot.log

# Error'larni filtrlash
grep "ERROR" logs/bot.log

# Specific foydalanuvchi uchun
grep "user_id=123456" logs/bot.log
```

### Database'ni Tekshirish

```python
import aiosqlite
import asyncio

async def check_db():
    db = await aiosqlite.connect('data/bot.db')
    
    # Guruhlarni ko'rish
    cursor = await db.execute("SELECT * FROM groups LIMIT 5")
    groups = await cursor.fetchall()
    print(groups)
    
    await db.close()

asyncio.run(check_db())
```

### Bot Status'ini Tekshirish

```bash
# Process'ni topish
ps aux | grep "python app.py"

# Port'ni tekshirish (polling uchun kerak emas)
netstat -tuln | grep :8080

# Resurslari tekshirish
top -p <PID>
```

---

## 🔐 Xavfsizlik Tekshiruvi

### Tokenni Tekshiring

```bash
# .env da token bor-yo'qligini tekshirish
if grep -q "BOT_TOKEN" .env; then
    echo "✓ Token topildi"
else
    echo "✗ Token yo'q"
fi
```

### Adminlar Ro'yxatini Tekshirish

```bash
# ADMINS qiymatini ko'rish
grep "ADMINS" .env

# Admin ID'larni tekshiring
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

### Permission'larni Tekshirung

```bash
# .env fayl permission'lari
ls -la .env
# Natija: -rw- r- r- (644)
```

---

## 🆘 SOS - Bosh Muammolar

### **Bot Suv­ma­yoti (Unresponsive)**

```bash
# 1. Bot jarayonini topish
pgrep -f "app.py"

# 2. Jarayonni o'ldirish
kill -9 <PID>

# 3. Qayta ishga tushirish
python app.py
```

### **Database Corrupt Boldi**

```bash
# Backup olish
cp data/bot.db data/bot.db.backup

# Yangi database yaratish
rm data/bot.db

# Bot qayta ishga tushirish (avtomatik baza yaratadi)
python app.py
```

### **Memory Leak (Xotirada MUAMMO)**

```bash
# Jarayonning xotira ishlatishini tekshirish
top -p <PID>

# Xotirani chekish
ulimit -v 1000000  # 1GB limit
```

---

## 📞 Qoshi Support

### Loglarni Yuborish

Xato haqida qo'imadigan bo'lsangiz, loglarni yuboringlar:

```bash
# Oxirgi 100 error'ni export qilish
grep "ERROR" logs/bot.log | tail -100 > error_report.log
```

Haqiqiy Telegram ID'larini loglardan o'chirib, anonymize qiling!

### Debugging Modu

```python
# app.py da
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✅ Tekshiruv Ro'yxati

Bot deploy qilishdan oldin tekshiruv qilingizar:

- [ ] BOT_TOKEN .env da to'g'ri
- [ ] ADMINS ro'yxati to'liq
- [ ] Database fayli borligini tekshiring
- [ ] Logs direktoriyasi borligi
- [ ] .env faylni .gitignore'ga qo'shing
- [ ] Barcha dependensiyalar o'rnatilgan
- [ ] Testlar o'tgan

---

Bu dokumentatsiyaga qo'shilishi geraki xatolar mavjud bo'lsa,
[Issue yarating](https://github.com/yourusername/groups-moderator-bot/issues)
