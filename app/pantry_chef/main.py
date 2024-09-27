from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import APIRouter, FastAPI

from pantry_chef.database import session_manager


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    if session_manager.has_engine():
        await session_manager.close()


app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix='/api/v1')


@app.get('/')
async def root() -> dict:
    return {'Hello': 'World'}


app.include_router(router)
