from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.event_repository import EventRepository
from app.schemas.event import Event

router = APIRouter(tags=["events"])


@router.post("/events")
async def create_event(event: Event, db: AsyncSession = Depends(get_db)):
    repository = EventRepository(db)
    event_raw = await repository.create(event.model_dump(mode="json"))
    await db.commit()
    return {"id": event_raw.id, "received_event": event}
