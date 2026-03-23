"""Filtrlarni ro'yxatdan o'tkazish."""
from aiogram import Dispatcher

from .admin import AdminFilter
from .chat_type import IsGroup, IsPrivate

__all__ = ["AdminFilter", "IsGroup", "IsPrivate", "setup"]


def setup(dp: Dispatcher):
    """Barcha filtrlarni Dispatcher'ga ro'yxatdan o'tkazadi."""
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
