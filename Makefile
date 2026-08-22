include .env.local

.PHONY: up down logs ps migrate local local-down local-logs local-ps local-reset local-db-shell local-migrate local-revision

COMPOSE_LOCAL = docker compose --env-file .env.local

# --- "Production" target: reads .env, talks to the AWS Postgres instance ---

up:
	docker compose up --build

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

# --- Local target: reads .env.local, talks to a Postgres installed
# natively on your machine (not Docker) — see .env.local for setup ---

local:
	$(COMPOSE_LOCAL) up --build

local-down:
	$(COMPOSE_LOCAL) down

local-logs:
	$(COMPOSE_LOCAL) logs -f

local-ps:
	$(COMPOSE_LOCAL) ps

# Drop and recreate the local database (clean slate). Talks to your native
# local Postgres directly, not a container.
local-reset:
	dropdb -h localhost -U $(POSTGRES_USER) --if-exists $(POSTGRES_DB)
	createdb -h localhost -U $(POSTGRES_USER) -O $(POSTGRES_USER) $(POSTGRES_DB)

local-db-shell:
	psql -h localhost -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# Applies alembic migrations inside the running local "master" container,
# against your native local Postgres.
local-migrate:
	$(COMPOSE_LOCAL) exec master uv run alembic upgrade head

# Autogenerates a new migration by diffing app/models/* against the local
# Postgres. Requires your native local Postgres to be running, since it
# connects to localhost:5432 from the host via uv.
# Usage: make local-revision m="create events_raw table"
local-revision:
	cd master && uv run alembic revision --autogenerate -m "$(m)"
