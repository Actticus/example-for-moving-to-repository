import pydantic
from pydantic import ConfigDict


class Base(pydantic.BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    @classmethod
    def properties_names(cls) -> list[str]:
        return list(cls.model_fields.keys())


class Identifier(Base):
    id: int


class UserPost(Base):
    first_name: str
    middle_name: str | None
    last_name: str
    phone: str


class UserGet(Base):
    first_name: str
    middle_name: str | None
    last_name: str
    phone: str
