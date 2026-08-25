from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demand_history import DemandHistory
from app.schemas.event import Event
from app.schemas.filters import DemandHistoryQuery

SORTABLE_COLUMNS = {
    "id": DemandHistory.id,
    "receivedAt": DemandHistory.received_at,
    "validUntil": DemandHistory.valid_until,
    "demand": DemandHistory.demand,
    "city": DemandHistory.city,
    "type": DemandHistory.type,
}


def _day_bounds(day: date) -> tuple[datetime, datetime]:
    """[inicio del dia, inicio del dia siguiente) en UTC."""
    start = datetime.combine(day, time.min, tzinfo=timezone.utc)
    return start, start + timedelta(days=1)


def _build_conditions(query: DemandHistoryQuery) -> list[ColumnElement[bool]]:
    """Traduce los filtros a condiciones SQL. Los ausentes (None) no aportan nada."""
    conditions: list[ColumnElement[bool]] = []

    if query.idpk is not None:
        conditions.append(DemandHistory.idpk == query.idpk)
    if query.type is not None:
        conditions.append(DemandHistory.type == query.type)
    if query.city is not None:
        conditions.append(DemandHistory.city == query.city)
    if query.unit is not None:
        conditions.append(DemandHistory.unit == query.unit)
    if query.meta_content is not None:
        conditions.append(DemandHistory.meta_content.ilike(f"%{query.meta_content}%"))

    if query.demand is not None:
        conditions.append(DemandHistory.demand == query.demand)
    if query.demand_min is not None:
        conditions.append(DemandHistory.demand >= query.demand_min)
    if query.demand_max is not None:
        conditions.append(DemandHistory.demand <= query.demand_max)

    for day, start_at, end_at, column in (
        (query.received_at, query.received_at_from, query.received_at_to, DemandHistory.received_at),
        (query.valid_until, query.valid_until_from, query.valid_until_to, DemandHistory.valid_until),
    ):
        if day is not None:
            start, end = _day_bounds(day)
            conditions.append(column >= start)
            conditions.append(column < end)
        if start_at is not None:
            conditions.append(column >= start_at)
        if end_at is not None:
            conditions.append(column <= end_at)

    return conditions


class DemandHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, id: int) -> DemandHistory | None:
        return await self.session.get(DemandHistory, id)

    async def count(self, query: DemandHistoryQuery) -> int:
        stmt = select(func.count()).select_from(DemandHistory).where(*_build_conditions(query))
        return await self.session.scalar(stmt) or 0

    async def search(self, query: DemandHistoryQuery) -> list[DemandHistory]:
        column = SORTABLE_COLUMNS[query.sort_by]
        order_by = [column.asc() if query.order == "asc" else column.desc()]
        # Desempate por id: sin un orden total, dos paginas consecutivas pueden
        # repetir u omitir filas cuando el campo ordenado empata. Ordenando por
        # id ya es total, asi que ahi el desempate sobraria.
        if query.sort_by != "id":
            order_by.append(DemandHistory.id.desc())
        stmt = (
            select(DemandHistory)
            .where(*_build_conditions(query))
            .order_by(*order_by)
            .offset((query.page - 1) * query.limit)
            .limit(query.limit)
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
