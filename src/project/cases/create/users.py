from dataclasses import dataclass

import sqlalchemy as sa

from . import base


@dataclass
class BulkCreateUsers(base.BulkCreate):
    phone_model: object

    async def validate(self):
        pass

    async def create_phones(self) -> dict[str, int | None]:
        phones = {}
        for patient in self.data:
            if patient.get("phone") is not None:
                phones[patient["phone"]] = None

        if phones:
            result = await self.session.execute(
                sa.select(
                    self.phone_model
                ).where(
                    self.phone_model.number.in_(phones.keys())
                )
            )
            existing_phones = result.scalars().all()

            for phone in existing_phones:
                phones[phone.number] = phone

            phones_to_create = {
                "number": number
                for number, phone_id in phones.items()
                if phone_id is None
            }
            if phones_to_create:
                result = await self.session.execute(
                    sa.insert(
                        self.phone_model
                    ).values(
                        phones_to_create
                    ).returning(
                        self.phone_model
                    )
                )
                created_phones = result.scalars().all()

                for phone in created_phones:
                    phones[phone.number] = phone
        return phones

    async def create(self):
        phones_by_number = await self.create_phones()
        for patient in self.data:
            number = patient.pop("phone", None)
            phone_id = phones_by_number[number].id if number else None
            patient["phone_id"] = phone_id
        patient_ids = await super().create()

        return patient_ids
