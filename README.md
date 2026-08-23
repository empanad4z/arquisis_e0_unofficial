# arquisis_e0_unofficial

Servicios (`docker-compose.yaml`):

- **postgres** — base de datos Postgres, corriendo como container propio.
- **master** — API FastAPI que recibe eventos y los persiste en Postgres.
- **connector** — consumidor de RabbitMQ (broker del curso).

## Setup

```sh
cp .env.example .env   # valores por defecto ya sirven, ajustalos si querés
make up                # build + levanta postgres, master y connector
make migrate           # aplica las migraciones de Alembic (primera vez)
```

`master` espera a que `postgres` esté `healthy` antes de arrancar. `postgres`
solo publica su puerto a `127.0.0.1:5432` (no al exterior) — accesible desde
el propio host para herramientas como `make db-shell` o `make revision`,
pero no expuesto a internet ni siquiera en la EC2.

## Comandos del Makefile

- `make up` — `docker compose up --build`. Levanta `postgres`, `master` y
  `connector`.
- `make start` / `make stop` — arranca/detiene los containers existentes
  sin reconstruirlos.
- `make down` — baja los containers (conserva el volumen de datos).
- `make reset` — igual, pero además borra el volumen (`-v`): Postgres
  completamente limpio en el próximo `make up`.
- `make logs` — sigue los logs de todos los servicios.
- `make ps` — estado de los containers.
- `make migrate` — corre `alembic upgrade head` **dentro** del container
  `master` que ya está corriendo, contra `postgres`. Requiere que `make up`
  esté levantado. Es una acción deliberada, no automática.
- `make revision m="mensaje"` — autogenera una migración de Alembic
  comparando los modelos (`master/app/models/*`) contra Postgres. Se corre
  en el host (no en Docker) usando `uv`, así no hace falta reconstruir la
  imagen cada vez que cambiás un modelo. Requiere que `postgres` esté
  arriba (`make up`, al menos el servicio `postgres`).
- `make db-shell` — abre un `psql` interactivo dentro del container
  `postgres`.

### Flujo típico de un cambio de esquema

```sh
make up                            # levanta postgres (y master)
# editás/agregás un modelo en master/app/models/
make revision m="agrega tabla X"   # genera master/alembic/versions/...
make migrate                       # la aplica, la revisás
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

## Deploy en EC2

En la EC2, nginx corre en el host (no containerizado) y hace de reverse
proxy hacia `master` (ver `nginx/api.empanad4z.me.conf`, publicado en
`localhost:8080` por `docker-compose.yaml`). El resto del stack —
`postgres` incluido — corre con `make up` igual que en cualquier otra
máquina.
