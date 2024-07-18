import abc
from dataclasses import dataclass

import sqlalchemy as sa

from .. import abstract


@dataclass
class BulkCreate(abstract.CaseDB):
    data: list[dict]
    model: object

    @abc.abstractmethod
    async def validate(self):
        pass

    async def create(self):
        result = await self.session.execute(
            sa.insert(
                self.model
            ).values(
                self.data
            ).returning(
                self.model.id
            )
        )
        await self.session.flush()
        return result.scalars().all()

    async def execute(self, *args, **kwargs):
        await self.validate()
        return await self.create()
