# Hissa Qoʻshish (Contributing)

## 🙋 Qanday Hissa Qoʻshish Mumkin?

Ushbu loyihaga hissa qoʻshishdan xursand bo'lamiz! Bularni qilish mumkin:

### 🐛 Xato Topish
- Xato topilsa, [Issues](https://github.com/yourusername/groups-moderator-bot/issues) yarating
- Xato tavsifi aniq yozing
- Qadam-qadam takrorlanish protokolini belgilaň

### ✨ Yangi Xususiyat
- Feature taklifi uchun [Discussions](https://github.com/yourusername/groups-moderator-bot/discussions) ishlatish tavsiya etiladi
- Batafsil tavsif yozing
- Nima uchun kerakligini tushuntiring

### 📝 Kodu Yaxshilash
- Dokumentatsiyani yaxshilang
- Xatolarni to'g'irlang
- Kodning sifatini oshiring

## 📋 Qo'shishdan Oldin

### 1. Loyihani Setup Qiling

```bash
# Forlang
git clone https://github.com/yourusername/groups-moderator-bot.git
cd groups-moderator-bot

# Virtual muhit
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements-dev.txt
```

### 2. .env Faylini Yarating

```bash
cp .env.dist .env
# .env ni tahrirlang va test bot token qo'shning
```

### 3. Kodni Tuzating

```bash
# Kodni tuzaring
black core/ handlers/ data/

# Xatolar uchun tekshiring
flake8 core/ handlers/ data/
pylint core/ handlers/ data/

# Type tekshiruvi
mypy core/ handlers/ data/
```

### 4. Testlar Yozish

```bash
# Test yarating
pytest tests/

# Coverage tekshiruvi
pytest --cov=core --cov=handlers
```

## 🔄 Pull Request Jarayoni

### 1. Feature Branch Yarating

```bash
git checkout -b feature/new-feature
# yoki
git checkout -b fix/bug-name
```

### 2. O'zgarishlarni Commit Qiling

```bash
# Qo'shish
git add .

# Commit (tavsif yozing)
git commit -m "feat: Add new moderation feature"
git commit -m "fix: Resolve warn system bug"
```

**Commit Message Formate:**
- `feat:` - Yangi xususiyat
- `fix:` - Xato tuzish
- `docs:` - Dokumentatsiya
- `refactor:` - Kod qayta yozish
- `test:` - Test qo'shish
- `chore:` - Utils, dependencies

### 3. Push va Pull Request

```bash
git push origin feature/new-feature
```

GitHub'da Pull Request yaratish uchun [PR Template](./pull_request_template.md) foydalaning.

## 📐 Kod Standartlari

### Python Kody Standartlar

- **PEP 8** standartiga amal qiling
- Line uzunligi: **88 belgigacha** (Black format)
- UTF-8 encoding foydalaning

### Naming Convention

```python
# Variables
my_variable = value
CONSTANT_VALUE = 100

# Functions
def my_function():
    pass

# Classes
class MyClass:
    pass

# Private methods
def _private_method():
    pass
```

### Dokumentatsiya

```python
def handle_warn(chat_id: int, user_id: int, reason: str) -> int:
    """
    Foydalanuvchiga ogohlantirsh qo'shadi.
    
    Args:
        chat_id: Guruh identifikatori
        user_id: Foydalanuvchi identifikatori
        reason: Ogohlantirsh sababi
    
    Returns:
        Ogohlantirshlar soni
    
    Raises:
        ValueError: Noto'g'ri parametrlar
    """
    pass
```

## 🧪 Testlar

### Test Qayta Ishga Tushirish

```bash
# Barcha testlar
pytest

# Specific fayl
pytest tests/test_filters.py

# Verbose mode
pytest -v

# Coverage
pytest --cov
```

### Test Yazmishning Namunasi

```python
import pytest
from core.database import models

@pytest.mark.asyncio
async def test_add_warn():
    """Ogohlantirsh qo'shish testi."""
    count = await models.add_warn(
        chat_id=123,
        user_id=456,
        user_name="testuser"
    )
    assert count == 1
```

## 🔍 Code Review Jarayoni

1. **Avtomat Tekshiruv**
   - Kodni tuzatish
   - Linting
   - Testlar

2. **Manual Review**
   - Kod sifati
   - Dokumentatsiya
   - Performance

3. **Merge**
   - Main branchga merge qilish
   - Release notes yangilash

## 📚 Foydalı Linklar

- [Loyiha Wiki](https://github.com/yourusername/groups-moderator-bot/wiki)
- [API Dokumentatsiya](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)

## ❓ Savollar?

- GitHub Discussions: [Discussions](https://github.com/yourusername/groups-moderator-bot/discussions)
- Email: your-email@example.com
- Telegram: @yourusername

---

**Hissa qoʻshganlar uchun rahmat!** 🙏
