from fastapi import FastAPI

from app.api.routes import events, health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(events.router)
