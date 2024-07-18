import fastapi
import sqlalchemy as sa
import sqlalchemy.ext.asyncio as sa_asyncio
from sqlalchemy import orm

from ... import cases
from ...adapters.db import models
from .. import sessions
from . import schemes


class Users:
    router = fastapi.APIRouter()

    @staticmethod
    @router.post(
        "",
        response_model=list[schemes.Identifier],
        status_code=201,
    )
    async def post(
        creating_users: list[schemes.UserPost],
        session: sa_asyncio.AsyncSession = fastapi.Depends(
            sessions.create_session
        ),
    ):
        case = cases.BulkCreateUsers(
            model=models.User,
            phone_model=models.Phone,
            data=[
                user.model_dump()
                for user in creating_users
            ],
            session=session
        )
        ids = await case.execute()
        return [{"id": id_} for id_ in ids]

    @staticmethod
    @router.get("", response_model=list[schemes.UserGet])
    async def get(
        ids: list[int] = fastapi.Query(),
        session: sa_asyncio.AsyncSession = fastapi.Depends(
            sessions.create_session
        ),
    ):
        result = await session.execute(
            sa.select(
                models.User
            ).where(
                sa.and_(
                    models.User.id.in_(ids),
                )
            ).options(
                orm.joinedload(models.User.phone),
            )
        )
        users = result.unique().scalars().all()

        return [
            schemes.UserGet.model_validate(user)
            for user in users
        ]
