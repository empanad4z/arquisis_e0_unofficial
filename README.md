# arquisis_e0_unofficial

## Para revisión E0

### Consideraciones generales

- **API / dominio:** https://api.empanad4z.me (documentación interactiva en `/docs`)
- **IP instancia EC2:** `35.168.184.246` (t3.micro, free tier)
- **Acceso SSH:** `ssh -i <archivo>.pem ubuntu@35.168.184.246`
- Prompts de IA usados durante el desarrollo documentados en `aidocs/prompts/`.
- **Configuración nginx utilizada (REPO/EC2)**: `nginx/api.empanad4z.me.conf` / `/etc/nginx/sites-available/api.empanad4z.me`
- **Por favor verificar que estás en la región `us-east-1` al momento de ingresar a la consola aws con credenciales.**

### Parte mínima

**Requisitos funcionales (10p)**

- [x] RF1 (3p, Esencial) `GET /history`: historial completo con todos los campos recibidos.
- [x] RF2 (1p) `GET /history/{id}`: detalle de un registro, `id` autogenerado por `master`.
- [x] RF3 (2p, Esencial) Paginación por defecto de 25 registros vía `page`/`limit`.
- [x] RF4 (4p, Esencial) Filtros por prácticamente todos los campos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exacto o rango, `validUntil` exacto o rango) más orden (`sortBy`, `order`).

**Requisitos no funcionales (20p)**

- [x] RNF1 (5p, Esencial) `connector` corre en container aparte, se conecta al broker por AMQP+SSL y reenvía cada evento a `master` por HTTP POST. Reintenta solo (sin intervención manual) si se pierde la conexión al broker; `master` sigue respondiendo consultas sobre lo ya guardado aunque el broker o `connector` estén caídos.
- [x] RNF2 (4p, Esencial) `master` en su propio container, recibe eventos de `connector` por POST, misma red docker.
- [x] RNF3 (3p) nginx como reverse proxy instalado directamente en el host EC2 (no en Docker), config (luego de instalar y configurar certbot) en `nginx/api.empanad4z.me.conf`. **Esta configuración en EC2 se encuentra en `/etc/nginx/sites-available/api.empanad4z.me`**
- [x] RNF4 (2p) dominio `api.empanad4z.me` bajo TLD público `.me`.
- [x] RNF5 (2p, Esencial) corriendo en EC2 free tier (t3.micro).
- [x] RNF6 (2p) Postgres containerizado, no expuesto a internet (solo `127.0.0.1`).
- [x] RNF7 (2p, Esencial) los 3 containers (`postgres`, `master`, `connector`) declaran `HEALTHCHECK` en `docker-compose.yaml` (`pg_isready`, chequeo HTTP a `/health`, y file-check respectivamente).

**Docker-Compose (15p)**

- [x] RNF1 (5p) `master` se levanta desde docker compose (con 2 réplicas).
- [x] RNF2 (5p) `postgres` integrado en el mismo `docker-compose.yaml`.
- [x] RNF3 (5p) `connector` se levanta desde docker compose y queda conectado a `master` por la red interna.

### Parte variable

Se optó por ambas opciones.

**HTTPS (25%, 15p)**

- [x] RNF1 (7p) dominio asegurado con SSL de Let's Encrypt.
- [x] RNF2 (3p) redirección automática HTTP → HTTPS.
- [x] RNF3 (5p) renovación automática del certificado usando configuración que venia en la instalación oficial en `https://certbot.eff.org/instructions?ws=nginx&os=pip`

**Balanceo de carga con Nginx (25%, 15p)**

- [x] RF1 (5p) `master` replicado en 2 instancias container en paralelo (`deploy.replicas: 2`).
- [x] RF2 (10p) cada réplica alcanzable individualmente (`8080-8081:8000`) y balanceadas por nginx vía `upstream` en `/etc/nginx/sites-available/api.empanad4z.me`.


Servicios (`docker-compose.yaml`):

- **postgres**: base de datos Postgres, corriendo como container propio.
- **master**: API FastAPI que recibe eventos y los persiste en Postgres.
- **connector**: consumidor de RabbitMQ (broker del curso).

## Setup

```sh
cp .env.example .env
make up                # build + levanta postgres, master y connector
make migrate           # aplica las migraciones de Alembic (primera vez)
```

## Comandos del Makefile

- `make up`: `docker compose up --build`. Levanta `postgres`, `master` y
  `connector`.
- `make start` / `make stop`: arranca/detiene los containers existentes
  sin reconstruirlos.
- `make down`: baja los containers (conserva el volumen de datos).
- `make reset`: igual, pero además borra el volumen (`-v`): Postgres
  completamente limpio en el próximo `make up`.
- `make logs`: sigue los logs de todos los servicios.
- `make ps`: estado de los containers.
- `make migrate`: corre `alembic upgrade head` **dentro** del container
  `master` que ya está corriendo, contra `postgres`. Requiere que `make up`
  esté levantado. Es una acción deliberada, no automática.
- `make revision m="mensaje"`: autogenera una migración de Alembic
  comparando los modelos (`master/app/models/*`) contra Postgres. Se corre
  en el host (no en Docker) usando `uv`, así no hace falta reconstruir la
  imagen cada vez que cambiás un modelo. Requiere que `postgres` esté
  arriba (`make up`, al menos el servicio `postgres`).
- `make db-shell`: abre un `psql` interactivo dentro del container
  `postgres`.

### Flujo típico de un cambio de esquema

```sh
make up
# editas/agregas un modelo en master/app/models/
make revision m="agrega tabla X"   # genera master/alembic/versions/...
make migrate                       # la aplica
```

## Base de datos

- ORM: **SQLAlchemy 2.0** (async, driver `asyncpg`) + **Alembic** para
  migraciones.
- Estructura en `master/app/`:
  - `models/`: entidades ORM (tablas).
  - `schemas/`: modelos Pydantic de entrada/salida de la API.
  - `repositories/`: acceso a datos (queries de SQLAlchemy).
  - `db/`: `base.py` (declarative base) y `session.py` (engine + sesión
    async, dependency `get_db` para FastAPI).
  - `alembic/`: migraciones (en `master/`, junto al `alembic.ini`).

## Deploy en EC2

En la EC2, nginx corre en el host (no containerizado) y hace de reverse
proxy hacia `master` (ver `nginx/api.empanad4z.me.conf`, publicado en
`localhost:8080-8081` por `docker-compose.yaml`). El resto del stack,
`postgres` incluido, corre con `make up` igual que en cualquier otra
máquina.
