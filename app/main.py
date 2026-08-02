from fastapi import FastAPI

from app.api.assistant import router as assistant_router
from app.api.auth import router as auth_router
from app.api.authorization import router as authorization_router
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.core.config import settings

app = FastAPI(title="LifeEasy")


@app.get("/")
def root():
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
    }


app.include_router(health_router)
app.include_router(assistant_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(authorization_router)
