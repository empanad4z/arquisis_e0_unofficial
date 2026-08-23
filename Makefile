.PHONY: up start stop down logs ps migrate db-shell local local-start local-stop local-down local-logs local-ps local-reset local-db-shell local-migrate local-revision

COMPOSE_LOCAL = docker compose -f docker-compose.yaml -f docker-compose.local.yaml --env-file .env.local

# --- "Production" target: reads .env, talks to the AWS Postgres instance ---

up:
	docker compose up --build

start:
	docker compose start

stop:
	docker compose stop

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

# Applies alembic migrations inside the running "master" container, against
# whatever DATABASE_URL that container currently has (i.e. the AWS DB).
migrate:
	docker compose exec master uv run alembic upgrade head

# Opens an interactive psql shell against the AWS RDS instance, using
# DATABASE_URL from ".env". Runs via a throwaway postgres:16-alpine
# container so nothing needs to be installed on the host (e.g. the EC2
# instance) — the "master" image itself doesn't ship a psql client.
db-shell:
	@url=$$(grep '^DATABASE_URL=' .env | cut -d= -f2- | sed 's/postgresql+asyncpg/postgresql/'); \
	docker run --rm -it postgres:16-alpine psql "$$url"

# --- Local target: reads .env.local, spins up a throwaway Postgres too ---

local:
	$(COMPOSE_LOCAL) up --build

local-start:
	$(COMPOSE_LOCAL) start

local-stop:
	$(COMPOSE_LOCAL) stop

local-down:
	$(COMPOSE_LOCAL) down

local-logs:
	$(COMPOSE_LOCAL) logs -f

local-ps:
	$(COMPOSE_LOCAL) ps

# Wipe the local Postgres volume (clean slate).
local-reset:
	$(COMPOSE_LOCAL) down -v

local-db-shell:
	$(COMPOSE_LOCAL) exec postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

# Applies alembic migrations inside the running local "master" container,
# against the local Postgres container.
local-migrate:
	$(COMPOSE_LOCAL) exec master uv run alembic upgrade head

# Autogenerates a new migration by diffing app/models/* against the local
# Postgres. Requires "make local" (or at least the postgres service) to be
# running, since it connects to localhost:5432 from the host via uv.
# Usage: make local-revision m="create events_raw table"
local-revision:
	cd master && uv run alembic revision --autogenerate -m "$(m)"
