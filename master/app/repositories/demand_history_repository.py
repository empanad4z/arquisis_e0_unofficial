from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demand_history import DemandHistory
from app.schemas.event import Event


class DemandHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, id: int) -> DemandHistory | None:
        return await self.session.get(DemandHistory, id)

    async def list_paginated(self, page: int, limit: int) -> list[DemandHistory]:
        offset = (page - 1) * limit
        stmt = (
            select(DemandHistory)
            .order_by(DemandHistory.id.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_from_event(self, event: Event) -> list[DemandHistory]:
        body = event.packageBody
        records = [
            DemandHistory(
                idpk=event.idpk,
                type=event.type,
                city=demand.city,
                demand=demand.demand,
                unit=demand.unit,
                valid_until=body.validUntil,
                meta_content=body.metaContent,
            )
            for demand in body.demands
        ]
        self.session.add_all(records)
        await self.session.flush()
        for record in records:
            await self.session.refresh(record)
        return records
