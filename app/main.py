from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()


@app.get("/")
def root():
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
