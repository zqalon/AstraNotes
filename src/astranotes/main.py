from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from astranotes.config import SECRET_KEY, SESSION_MAX_AGE
from astranotes.db import init_db
from astranotes.routes import router

app = FastAPI(title="AstraNotes")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=SESSION_MAX_AGE)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).resolve().parent / "static"),
    name="static",
)
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    init_db()
