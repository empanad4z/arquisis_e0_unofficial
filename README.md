# arquisis_e0_unofficial

## Comandos del Makefile

### Producción / AWS (usa `.env`)

- `make up` — `docker compose up --build`. Levanta `master` + `connector`
  contra la base de AWS.
- `make down` — baja los contenedores.
- `make logs` — sigue los logs de todos los servicios.
- `make ps` — estado de los contenedores.
- `make migrate` — corre `alembic upgrade head` **dentro** del contenedor
  `master` que ya está corriendo, contra la base de AWS. Requiere que
  `make up` esté levantado. Es una acción deliberada, no automática, porque
  toca la base de datos compartida.

### Local (usa `.env.local`, Postgres descartable)

- `make local` — `docker compose -f docker-compose.yaml -f
  docker-compose.local.yaml --env-file .env.local up --build`. Levanta
  `master`, `connector` y un Postgres local (`postgres:16-alpine`) con
  healthcheck; `master` espera a que el Postgres esté `healthy` antes de
  arrancar.
- `make local-down` — baja el stack local (conserva el volumen de datos).
- `make local-reset` — igual, pero además borra el volumen (`-v`): base de
  datos local completamente limpia en el próximo `make local`.
- `make local-logs` / `make local-ps` — logs / estado del stack local.
- `make local-db-shell` — abre un `psql` interactivo contra el Postgres
  local (adentro del contenedor `postgres`).
- `make local-migrate` — corre `alembic upgrade head` dentro del contenedor
  `master` local, contra el Postgres local.
- `make local-revision m="mensaje"` — autogenera una migración de Alembic
  comparando los modelos (`master/app/models/*`) contra el Postgres local.
  Se corre en el host (no en Docker) usando `uv`, así no hace falta
  reconstruir la imagen cada vez que cambiás un modelo. Requiere que el
  Postgres local esté arriba (`make local` o al menos el servicio
  `postgres`).

### Flujo típico de un cambio de esquema

```sh
make local                              # levanta Postgres local (y master)
# editás/agregás un modelo en master/app/models/
make local-revision m="agrega tabla X"  # genera master/alembic/versions/...
make local-migrate                      # la aplica en local, la revisás
# commit + push
make migrate                            # la aplica en AWS, cuando estés listo
```

## Base de datos

- ORM: **SQLAlchemy 2.0** (async, driver `asyncpg`) + **Alembic** para
  migraciones.
- Estructura en `master/app/`:
  - `models/` — entidades ORM (tablas).
  - `schemas/` — modelos Pydantic de entrada/salida de la API.
  - `repositories/` — acceso a datos (queries de SQLAlchemy).
  - `db/` — `base.py` (declarative base) y `session.py` (engine + sesión
    async, dependency `get_db` para FastAPI).
  - `alembic/` — migraciones (en `master/`, junto al `alembic.ini`).