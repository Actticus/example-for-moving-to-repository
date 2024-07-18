from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import orm

from . import mixins


class Phone(
    mixins.IntPrimaryKey,
    mixins.Base,
):
    number: orm.Mapped[str] = orm.mapped_column(
        sa.String(length=16),
        nullable=False,
    )

    # Reverse relations
    users: orm.Mapped[list[User]] = orm.relationship(
        "User",
        back_populates="phone",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        sa.Index(
            'phone_number_idx',
            number,
        ),
    )

    def __str__(self) -> str:
        return str(self.number)


class User(
    mixins.IntPrimaryKey,
    mixins.Password,
    mixins.Base,
):
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(length=128))
    middle_name: orm.Mapped[str] = orm.mapped_column(sa.String(length=128))
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String(length=128))

    # Relations
    phone_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey(
            'phone.id',
            ondelete='cascade',
            name='user_phone_id_fkey',
        ),
    )

    # Reverse relations
    phone: orm.Mapped[Phone] = orm.relationship(
        "Phone",
        uselist=False,
        back_populates="users",
    )

    # Indexes
    __table_args__ = (
        sa.Index(
            'user_phone_id_idx',
            phone_id,
        ),
    )
