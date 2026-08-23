from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "master"
    # Matches the Postgres container in docker-compose.yaml (service
    # "postgres", published to 127.0.0.1:5432). Docker Compose always
    # injects a real DATABASE_URL for the "master" container itself, so this
    # default is only ever used when running outside a container on the host
    # (e.g. `uv run pytest`, `make revision`).
    database_url: str = "postgresql+asyncpg://master:master@localhost:5432/master"


settings = Settings()
