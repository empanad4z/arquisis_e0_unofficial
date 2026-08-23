import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.event_repository import EventRepository
from app.schemas.event import Event

logger = logging.getLogger(__name__)

router = APIRouter(tags=["events"])


@router.post("/events")
async def create_event(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Body no es JSON valido")
        
    try:
        Event.model_validate(payload)
    except ValidationError as exc:
        logger.warning("Evento no calza con el schema Event, se descarta: %s", exc.errors())
        raise HTTPException(status_code=422, detail=exc.errors())

    repository = EventRepository(db)
    event_raw = await repository.create(payload)
    await db.commit()
    return {"id": event_raw.id}
