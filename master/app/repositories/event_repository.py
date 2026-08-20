from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_raw import EventRaw


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: dict) -> EventRaw:
        event_raw = EventRaw(payload=payload)
        self.session.add(event_raw)
        await self.session.flush()
        await self.session.refresh(event_raw)
        return event_raw
