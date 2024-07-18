import sqlalchemy.ext.asyncio as sa_asyncio

from .. import settings


class Database:
    _ENGINE = None

    @classmethod
    def init(cls):
        cls._ENGINE = sa_asyncio.create_async_engine(
            settings.DATABASE_ASYNC_URL,
        )

    @classmethod
    def get(cls):
        if cls._ENGINE is None:
            cls.init()
        return cls._ENGINE
