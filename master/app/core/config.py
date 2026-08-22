from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "master"
    # Matches the local Postgres spun up by "make local" (see .env.local).
    # Docker Compose always injects a real DATABASE_URL, so this default is
    # only ever used when running outside a container (e.g. `uv run pytest`,
    # `make local-revision`).
    database_url: str = "postgresql+asyncpg://master:master@localhost:5432/master"


settings = Settings()
