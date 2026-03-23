"""
Multi-til tizimi.
Faqat get_text() funksiyasi va til fayllarini import qilish.
"""
from core.locales.uz import STRINGS as UZ
from core.locales.ru import STRINGS as RU
from core.locales.en import STRINGS as EN

LANGUAGES = {
    "uz": UZ,
    "ru": RU,
    "en": EN,
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """
    Berilgan til va kalit bo'yicha matn qaytaradi.
    Agar topilmasa, o'zbekcha variant qaytariladi.
    """
    strings = LANGUAGES.get(lang, UZ)
    text = strings.get(key, UZ.get(key, key))

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass

    return text
