from fastapi import APIRouter

from app.models.event import Event

router = APIRouter(tags=["events"])


@router.post("/events")
async def create_event(event: Event):
    return {"received_event": event}
