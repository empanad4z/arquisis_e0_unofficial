.PHONY: up start stop down logs ps migrate revision db-shell reset

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
# the "postgres" container.
migrate:
	docker compose exec master uv run alembic upgrade head

# Autogenerates a new migration by diffing app/models/* against Postgres.
# Runs on the host (not in Docker) via uv, so it doesn't need an image
# rebuild every time a model changes. Connects through the port
# docker-compose.yaml publishes to 127.0.0.1. Requires "make up" (or at
# least the "postgres" service) to be running.
# Usage: make revision m="create events_raw table"
revision:
	cd master && uv run alembic revision --autogenerate -m "$(m)"

# Opens an interactive psql shell against the "postgres" container.
db-shell:
	docker compose exec postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

# Wipe the Postgres volume (clean slate).
reset:
	docker compose down -v
