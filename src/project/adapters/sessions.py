from collections.abc import AsyncGenerator

import sqlalchemy.ext.asyncio as sa_asyncio
from sqlalchemy import orm

from . import engines


def get_session_class():
    engine = engines.Database.get()
    return orm.sessionmaker(
        engine,
        expire_on_commit=False,
        class_=sa_asyncio.AsyncSession,
    )


async def create_session() -> AsyncGenerator[sa_asyncio.AsyncSession, None]:
    session_class = get_session_class()
    session: sa_asyncio.AsyncSession = session_class()

    try:
        yield session
    except Exception as e:
        await session.rollback()  # pragma: nocover
        await session.close()  # pragma: nocover
        raise e  # pragma: nocover
    await session.commit()
    await session.close()
