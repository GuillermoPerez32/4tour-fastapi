from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.database import init_db
from app.routers import users, travels


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(travels.router)
