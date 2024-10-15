from typing import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app.pantry_chef.database import get_db_session
from app.pantry_chef.main import app as actual_app


@pytest.fixture(autouse=True)
def app() -> FastAPI:
    actual_app.dependency_overrides[get_db_session] = lambda: None
    return actual_app


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
            transport=ASGITransport(app=app),  # type: ignore
            base_url='http://test'
    ) as _client:
        yield _client
