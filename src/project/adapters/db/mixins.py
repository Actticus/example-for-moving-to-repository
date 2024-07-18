import re

import bcrypt
from sqlalchemy import orm
from sqlalchemy.ext import declarative as sa_declarative


class Base(orm.DeclarativeBase):

    @sa_declarative.declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return '_'.join(re.findall('[A-Z][^A-Z]*', cls.__name__)).lower()


class IntPrimaryKey:
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)


class Password:

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(  # pylint: disable=attribute-defined-outside-init
            password=bytes(password, "ascii"),
            salt=bcrypt.gensalt(),
        )

    def is_right_password(self, password: str):
        return bcrypt.checkpw(
            password=bytes(password, "ascii"),
            hashed_password=self.password,
        )
