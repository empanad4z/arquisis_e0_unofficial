# arquisis_e0_unofficial

## Comandos del Makefile

Se utiliza un Makefile para hacer breves los comandos utiles y explicitar el uso de la conexión a la base de datos local (ver sección "Local" del por qué quiero tenerla al momento de desarrollar y probar cosas).

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

### Local - Desarrollo (usa `.env.local`, Postgres nativo — sin contenedor)

Para desarrollo local no se levanta ningún contenedor de Postgres o se utiliza la RDS de Amazon. **Esto se hace para evitar utilizar la RDS de AWS y disminuir el consumo de créditos. Considerar que la entrega en EC2 SOLO va a utilizar la RDS, sin levantar una base de datos en un contenedor o tenerla creada en la máquina.**

Setup inicial:

```sh
sudo apt install postgresql                # o `brew install postgresql`, etc.
sudo -u postgres createuser -P master       # password: master
sudo -u postgres createdb -O master master
```

- `make local` — `docker compose --env-file .env.local up --build`. Levanta
  `master` y `connector`, apuntando a Postgres local vía
  `host.docker.internal`.
- `make local-down` — baja el stack local.
- `make local-reset` — hace `dropdb`/`createdb` contra Postgres local
  (desde el host): base de datos local completamente limpia.
- `make local-logs` / `make local-ps` — logs / estado del stack local.
- `make local-db-shell` — abre un `psql` interactivo contra Postgres
  local (desde el host, no requiere Docker).
- `make local-migrate` — corre `alembic upgrade head` dentro del contenedor
  `master` local, contra Postgres local.
- `make local-revision m="mensaje"` — autogenera una migración de Alembic
  comparando los modelos (`master/app/models/*`) contra el Postgres local.
  Se corre en el host (no en Docker) usando `uv`, así no hace falta
  reconstruir la imagen cada vez que se cambia un modelo. Requiere que que
  Postgres local esté corriendo (el servicio del sistema, no un contenedor).

### Flujo típico de un cambio de esquema

```sh
make local                              # levanta master/connector (Postgres local ya corre como servicio del sistema)
# editas/agregas un modelo en master/app/models/
make local-revision m="agrega tabla X"  # genera master/alembic/versions/...
make local-migrate                      # la aplica en local
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