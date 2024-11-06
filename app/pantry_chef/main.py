from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import (
    APIRouter,
    FastAPI,
)

from pantry_chef.database import session_manager
from pantry_chef.ingredient.api import router as ingredient_router
from pantry_chef.instruction.api import router as instruction_router
from pantry_chef.recipe.api import router as recipe_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    if session_manager.has_engine():
        await session_manager.close()


app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix='/api/v1')


@app.get('/')
async def root() -> dict[str, str]:
    return {'Hello': 'World'}


router.include_router(recipe_router)
router.include_router(instruction_router)
router.include_router(ingredient_router)
app.include_router(router)
