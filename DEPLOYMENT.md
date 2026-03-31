# 🚀 Deployment Guide

Ushbu qo'llanma loyihani production'ga deploy qilishni ko'rsatadi.

## 📋 Talablar

- Linux/MacOS server (Ubuntu 20.04+ tavsiya etiladi)
- Python 3.8+
- systemd (Linux)
- SQLite3
- Git

## 1️⃣ Server Tayyorlash

### Ubuntu/Debian'da Server Tayyorlash

```bash
# System yangilash
sudo apt update && sudo apt upgrade -y

# Python va zarur paketlarni o'rnatish
sudo apt install -y python3.10 python3-pip python3-venv git

# Bot uchun user yaratish
sudo useradd -m -s /bin/bash moderator
sudo su - moderator
```

## 2️⃣ Loyihani Klonlash

```bash
# Repositoriyani klonlash
git clone https://github.com/yourusername/groups-moderator-bot.git
cd groups-moderator-bot

# Virtual muhit yaratish
python3 -m venv venv
source venv/bin/activate

# Dependencies o'rnatish
pip install -r requirements.txt
```

## 3️⃣ Environment Sozlash

```bash
# .env faylini yaratish
cp .env.dist .env

# Tahrirlash (nano yoki vi)
nano .env
```

**.env nizolama:**
```env
BOT_TOKEN=your_token_here
ADMINS=12345678,87654321
ip=192.168.1.1
DATABASE_URL=/home/moderator/groups-moderator-bot/data/bot.db
LOGS_DIR=/home/moderator/groups-moderator-bot/logs
LOG_LEVEL=INFO
```

## 4️⃣ Systemd Service Yaratish

### Service Faylini Yaratish

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

**Content:**
```ini
[Unit]
Description=Telegram Groups Moderator Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=moderator
WorkingDirectory=/home/moderator/groups-moderator-bot
Environment="PATH=/home/moderator/groups-moderator-bot/venv/bin"
ExecStart=/home/moderator/groups-moderator-bot/venv/bin/python /home/moderator/groups-moderator-bot/app.py

# Avtomatik qayta ishga tushirish
Restart=always
RestartSec=10
StartLimitInterval=60s
StartLimitBurst=3

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=telegram-bot

[Install]
WantedBy=multi-user.target
```

### Service'ni Ishga Tushirish

```bash
# Service faylini yangilash
sudo systemctl daemon-reload

# Botni ishga tushirish
sudo systemctl start telegram-bot

# Status tekshirish
sudo systemctl status telegram-bot

# Boot'da avtomatik ishga tushirilsin
sudo systemctl enable telegram-bot
```

## 5️⃣ Monitoring va Backup

### Loglarni Kuzatish

```bash
# Real-time log
sudo journalctl -u telegram-bot -f

# Oxirgi 100 qator
sudo journalctl -u telegram-bot -n 100
```

### Backup Script Yaratish

`backup.sh` faylini yarating:

```bash
#!/bin/bash

BACKUP_DIR="/home/moderator/backups"
BOT_DIR="/home/moderator/groups-moderator-bot"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# Backup direktoriyasini yaratish
mkdir -p $BACKUP_DIR

# Database backup
cp $BOT_DIR/data/bot.db $BACKUP_DIR/bot_${DATE}.db

# Logs backup
tar -czf $BACKUP_DIR/logs_${DATE}.tar.gz $BOT_DIR/logs/

# Eski backup'larni o'chirish (30 kundan ko'eski)
find $BACKUP_DIR -name "bot_*.db" -mtime +30 -delete
find $BACKUP_DIR -name "logs_*.tar.gz" -mtime +30 -delete

echo "Backup created: $DATE"
```

### Cron Job Qo'shish

```bash
# Crontab'ni tahrirlash
crontab -e

# Har kun 2:00 AM da backup olish
0 2 * * * /home/moderator/groups-moderator-bot/backup.sh
```

## 6️⃣ SSL/TLS (Optional - Webhook uchun)

Agar webhook ishlatsangiz:

```bash
# Let's Encrypt orqali sertifikat olish
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

Nginx reverse proxy'ni sozlash:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 7️⃣ Production Best Practices

### Performance Optimization

1. **Database**
   ```bash
   # WAL (Write-Ahead Logging) yoqilgan
   # Allaqachon app'da sozlangan
   ```

2. **Memory**
   - MemoryStorage'ni Redis/RedisSupport'ga almashtiring (production uchun)

3. **Rate Limiting**
   - Telegram API limits ga e'tibor bering
   - Massive requests uchun queue system qo'llanilsin

### Security Measures

1. **Firewall**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **.env Security**
   ```bash
   # .env faylining ruxsatini qo'yish
   chmod 600 /home/moderator/groups-moderator-bot/.env
   ```

3. **Regular Updates**
   ```bash
   cd /home/moderator/groups-moderator-bot
   git pull origin main
   pip install -r requirements.txt
   sudo systemctl restart telegram-bot
   ```

## 8️⃣ Troubleshooting

### Bot ishga tusmaydi

```bash
# Service statusni tekshirish
sudo systemctl status telegram-bot

# Errorlarni ko'rish
sudo journalctl -u telegram-bot -n 50 --no-pager

# Manual test
source venv/bin/activate
python app.py
```

### Database xatoligi

```bash
# Database permissions
sudo chown moderator:moderator /home/moderator/groups-moderator-bot/data/
sudo chmod 755 /home/moderator/groups-moderator-bot/data/

# WAL files tekshirish
ls -la data/
```

### Memory o'sishi

```bash
# Memory usage ko'rish
ps aux | grep python | grep app.py
# Agar o'zboshimchalik o'rdim, service qayta ishga tushurilsin
```

## 9️⃣ Scaling (Katta loyihalar uchun)

### Multi-Instance Setup

Agar bir nechta bot instansi kerak bo'lsa:

1. **Database ni centralized qiling**
   ```python
   # PostgreSQL yoki MySQL ishlatish
   # aiosqlite o'rniga
   ```

2. **Session storage**
   ```python
   # RedisStorage ishlatish
   from aiogram.contrib.fsm_storage.redis import RedisStorage
   ```

3. **Load Balancer**
   - Nginx yoki HAProxy

## 🔄 Update Jarayoni

```bash
# 1. Service'ni to'xtatish
sudo systemctl stop telegram-bot

# 2. Kodni yangilash
cd /home/moderator/groups-moderator-bot
git pull origin main

# 3. Dependencies yangilash
source venv/bin/activate
pip install -r requirements.txt

# 4. Service'ni qayta ishga tushirish
sudo systemctl start telegram-bot

# 5. Status tekshirish
sudo systemctl status telegram-bot
```

## 📊 Monitoring Dashboard (Optional)

Prometheus + Grafana setup:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'telegram-bot'
    static_configs:
      - targets: ['localhost:8000']
```

---

**Bu deployment production'da turli serverlar uchun. Sizning konfiguratsiyangizga qarab o'zgartirishliz mumkin!**
