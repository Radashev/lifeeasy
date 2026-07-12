from fastapi import FastAPI

from app.api.assistant import router as assistant_router
from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI()


@app.get("/")
def root():
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
    }


app.include_router(health_router)
app.include_router(assistant_router)