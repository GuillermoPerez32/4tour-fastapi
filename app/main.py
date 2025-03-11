from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from app.database.database import init_db
from app.routers import users, travels, files


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(travels.router)
app.include_router(files.router)

app.mount("/public", StaticFiles(directory="public"), name="public")
