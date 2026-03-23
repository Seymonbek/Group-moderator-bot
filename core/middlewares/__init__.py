"""Middleware'larni ro'yxatdan o'tkazish."""
from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .anti_flood import AntiFloodMiddleware
from .stats_counter import StatsCounterMiddleware

__all__ = ["ThrottlingMiddleware", "AntiFloodMiddleware", "StatsCounterMiddleware", "setup"]


def setup(dp: Dispatcher):
    """Barcha middleware'larni Dispatcher'ga ulaydi."""
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(AntiFloodMiddleware())
    dp.middleware.setup(StatsCounterMiddleware())
