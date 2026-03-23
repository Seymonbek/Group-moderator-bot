def rate_limit(limit: int, key=None):
    """
    Handler uchun throttling cheklovini belgilash dekoratori.
    ThrottlingMiddleware bilan birgalikda ishlaydi.

    Ishlatilishi:
        @rate_limit(5)
        @dp.message_handler(...)
        async def handler(message): ...
    """

    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator
