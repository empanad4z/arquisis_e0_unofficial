import json
import logging
import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.demand_history_repository import DemandHistoryRepository
from app.schemas.demand_history import DemandHistoryOut, Page
from app.schemas.event import Event
from app.schemas.filters import DemandHistoryQuery

logger = logging.getLogger(__name__)

router = APIRouter(tags=["events"])


@router.post("/events")
async def create_event(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Body no es JSON valido")

    try:
        event = Event.model_validate(payload)
    except ValidationError as exc:
        logger.warning("Evento no calza con el schema Event, se descarta: %s", exc.errors())
        raise HTTPException(status_code=422, detail=exc.errors())

    repository = DemandHistoryRepository(db)
    records = await repository.create_from_event(event)
    await db.commit()
    return {"ids": [record.id for record in records]}


@router.get("/history/{id}", response_model=DemandHistoryOut)
async def find_event(id: int, db: AsyncSession = Depends(get_db)):
    repository = DemandHistoryRepository(db)
    record = await repository.find_by_id(id)
    if record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record


@router.get("/history", response_model=Page[DemandHistoryOut])
async def show_events(
    query: Annotated[DemandHistoryQuery, Query()],
    db: AsyncSession = Depends(get_db),
):
    repository = DemandHistoryRepository(db)
    total = await repository.count(query)
    items = await repository.search(query)
    return Page(
        items=items,
        total=total,
        page=query.page,
        limit=query.limit,
        pages=math.ceil(total / query.limit),
    )
