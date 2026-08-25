from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DemandHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    idpk: str
    type: str
    city: str
    demand: float
    unit: str
    valid_until: datetime
    meta_content: str | None
    received_at: datetime


class Page[T](BaseModel):
    """Respuesta paginada generica: los items mas la metadata para navegar."""

    items: list[T]
    total: int
    page: int
    limit: int
    pages: int
