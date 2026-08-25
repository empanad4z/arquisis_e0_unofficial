from datetime import date, datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

SortField = Literal["id", "receivedAt", "validUntil", "demand", "city", "type"]


class DemandHistoryQuery(BaseModel):
    """Filtros + paginacion del endpoint GET /history.

    Se declara como modelo Pydantic para poder pasarlo entero como
    Annotated[DemandHistoryQuery, Query()]. Los alias camelCase permiten
    ?receivedAt=2025-08-08 mientras el codigo interno usa snake_case.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        # Rechaza query params desconocidos con 422 en vez de ignorarlos:
        # asi un typo como ?recievedAt=... falla ruidosamente.
        extra="forbid",
    )

    # --- Filtros por igualdad ---
    idpk: str | None = None
    type: str | None = None
    city: str | None = None
    unit: str | None = None

    # --- Texto parcial (case-insensitive) ---
    meta_content: str | None = None

    # --- Numericos: exacto o rango ---
    demand: float | None = None
    demand_min: float | None = None
    demand_max: float | None = None

    # --- Tiempo: un dia completo (date) o un rango preciso (datetime) ---
    received_at: date | None = Field(
        default=None,
        description="Filtra por dia completo en UTC. Ej: 2025-08-08",
    )
    received_at_from: datetime | None = None
    received_at_to: datetime | None = None

    valid_until: date | None = None
    valid_until_from: datetime | None = None
    valid_until_to: datetime | None = None

    # --- Orden y paginacion ---
    sort_by: SortField = "id"
    order: Literal["asc", "desc"] = "desc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=25, ge=1, le=100)

    @field_validator("received_at_from", "received_at_to", "valid_until_from", "valid_until_to")
    @classmethod
    def assume_utc(cls, value: datetime | None) -> datetime | None:
        """Un datetime sin zona horaria se interpreta como UTC.

        Las columnas son TIMESTAMPTZ; comparar contra un datetime naive
        haria fallar (o peor, desplazar) la consulta.
        """
        if value is not None and value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
