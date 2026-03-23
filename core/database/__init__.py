"""
Ma'lumotlar bazasi bilan ishlash moduli.
Tashqi fayllar faqat shu yerdan import qiladi.
"""
from core.database.connection import get_db, close_db
from core.database.schema import init_db

__all__ = ["get_db", "close_db", "init_db"]
