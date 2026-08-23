# arquisis_e0_unofficial

## Comandos del Makefile

Se utiliza un Makefile para hacer breves los comandos utiles y explicitar el uso de la conexión a la base de datos local (ver sección "Local" del por qué quiero tenerla al momento de desarrollar y probar cosas).

### Producción / AWS (usa `.env`)

- `make up` — `docker compose up --build`. Levanta `master` + `connector`
  contra la base de AWS.
- `make start` / `make stop` — arranca/detiene los contenedores existentes
  sin reconstruirlos (`docker compose start`/`stop`).
- `make down` — baja los contenedores.
- `make logs` — sigue los logs de todos los servicios.
- `make ps` — estado de los contenedores.
- `make migrate` — corre `alembic upgrade head` **dentro** del contenedor
  `master` que ya está corriendo, contra la base de AWS. Requiere que
  `make up` esté levantado. Es una acción deliberada, no automática, porque
  toca la base de datos compartida.
- `make db-shell` — abre un `psql` interactivo contra la RDS de AWS, usando
  el `DATABASE_URL` de `.env`. Corre vía un contenedor descartable
  `postgres:16-alpine` (la imagen de `master` no trae cliente `psql`), así
  que solo requiere Docker en el host — pensado para usarse desde la EC2 una
  vez que ya tiene conectividad con la RDS.

### Local - Desarrollo (usa `.env.local`, Postgres descartable en Docker)

Para desarrollo local se levanta un contenedor de Postgres con Docker
Compose en vez de usar la RDS de Amazon. **Esto se hace para evitar utilizar
la RDS de AWS y disminuir el consumo de créditos. Considerar que la entrega
en EC2 SOLO va a utilizar la RDS, sin levantar una base de datos en un
contenedor o tenerla creada en la máquina.** Al ser un contenedor (no una
instalación nativa en el host), el setup es el mismo para cualquier
desarrollador del equipo — no depende de tener Postgres instalado en la
máquina de cada uno.

- `make local` — `docker compose -f docker-compose.yaml -f
  docker-compose.local.yaml --env-file .env.local up --build`. Levanta
  `master`, `connector` y un Postgres local (`postgres:16-alpine`) con
  healthcheck; `master` espera a que el Postgres esté `healthy` antes de
  arrancar.
- `make local-start` / `make local-stop` — arranca/detiene los contenedores
  del stack local existentes sin reconstruirlos.
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