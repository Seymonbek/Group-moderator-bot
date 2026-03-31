# ⚡ Tezkor Boshlash (Quick Start)

Bu qo'llanma 5 daqiqada botni ishga tushirish uchun.

## 1️⃣ Asosiy Talablar

```bash
# Python 3.8+ o'rnatilganini tekshiring
python3 --version
# Natija: Python 3.10.x
```

## 2️⃣ Loyihani Klonlash

```bash
git clone https://github.com/yourusername/groups-moderator-bot.git
cd groups-moderator-bot
```

## 3️⃣ Virtual Muhit

```bash
# Virtual muhit yaratish
python3 -m venv venv

# Aktivlash (Linux/Mac)
source venv/bin/activate

# YOKI Windows
venv\Scripts\activate
```

## 4️⃣ Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

## 5️⃣ Bot Token Olish

1. Telegram'da **[@BotFather](https://t.me/BotFather)** ga yozing
2. `/newbot` buyrugi yuboring
3. Bot nomini va @username'ni yozing
4. **Token**ni ko'ching (masalan: `1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij`)

## 6️⃣ Admin ID Topish

1. [@userinfobot](https://t.me/userinfobot) ga yozing
2. O'zingizning ID'ni bilib oling (masalan: `123456789`)

## 7️⃣ .env Faylini Sozish

```bash
# .env.dist'dan .env yaratish
cp .env.dist .env

# Notepad/nano/vi bilan tahrirlash
nano .env
```

### .env kontent:
```env
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij
ADMINS=123456789
ip=localhost
```

## 8️⃣ Botni Ishga Tushirish

```bash
python app.py
```

**Sukses'ni ko'rsatguvchi natija:**
```
INFO: Bot muvaffaqiyatli ishga tushdi!
```

## 9️⃣ Test Qiling

1. Telegram'da bu bot'ini qoplang: `@yourbotusername`
2. `/start` yuboding
3. `/help` yuboding

## 🔟 Guruhda Test Qilish

1. Telegram'da yangi guruh yarating
2. Bot'ni guruhga qo'shing
3. Bot admin qiling
4. Admin buyruqlarni test qiling:
   ```
   /anti_link
   /anti_flood
   /settings
   ```

---

## 🔧 Umumiy Buyruqlar

### Foydalanuvchi Buyruqlari
```
/start     - Botni boshlash
/help      - Yordam
/settings  - Sozlamalar
```

### Admin Buyruqlari
```
/warn @user [sababi]        - Ogohlantirsh
/unwarn @user               - Ogohlantirshni bekor qilish
/ban @user [sababi]         - Ban qilish
/kick @user                 - Olib tashlash
/mute @user [vaqt]          - Jim qilish
```

### Xususiyatlarni Boshqarish
```
/anti_link              - Linklar blokirovkasi
/anti_flood             - Flood blokirovkasi
/anti_bot               - Bot blokirovkasi
/captcha                - CAPTCHA tekshiruvi
/max_warns 3            - Maksimal ogohlantirshlar
```

---

## ❌ Umumiy Xatolar

### **Xato 1: `BOT_TOKEN is invalid`**

```
❌ BOT_TOKEN .env da noto'g'ri!
✅ @BotFather'dan qayta oling
```

### **Xato 2: `ADMINS is empty`**

```
❌ Admin ID'si yo'q
✅ @userinfobot'dan ID topib, .env'ga yozing
```

### **Xato 3: `ModuleNotFoundError: No module named 'aiogram'`**

```bash
# Dependensiyalarni o'rnatmadingiz
pip install -r requirements.txt
```

### **Xato 4: Bot Javob Bermaydi**

```
1. Bot processini tekshirish
   ps aux | grep python

2. Bot qayta ishga tushirish
   Ctrl+C → python app.py

3. Log'larni tekshirish (agar sohilagi bo'lsa)
   tail -f logs/bot.log
```

---

## 📚 Ko'proq Qo'llanmalar

- **[README.md](README.md)** - To'liq hujjat
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production'ga chiqarish
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Muammolarni tuzatish
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development

---

## 🎓 Kiyingi Qadamlar

1. **Konfiguratsiyani O'zgaritirish**
   - Xususiyatlarni yoqib-o'chirish
   - Flood cheklovi o'zgaritirish

2. **Database'ni Tekshirish**
   - Group settings'larini ko'rish
   - User statistics'larni tekshirish

3. **Logging Sozlash**
   - Log channel yaratish
   - Bot'ni admin qilish

4. **Production'ga Deploy Qilish**
   - Server'da o'rnatish
   - Systemd service sozlash

---

💡 **Savol bo'lsa, [TROUBLESHOOTING.md](TROUBLESHOOTING.md)'ga qarang!**
