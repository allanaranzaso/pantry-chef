from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from pantry_chef.config import settings

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: Optional[Dict[str, Any]] = None) -> None:
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    def has_engine(self) -> bool:
        return self._engine is not None

    async def close(self) -> None:
        if self._engine is None:
            raise Exception('Database engine is not set')

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception('Database engine is not set')

        async with self._engine.begin() as connection:
            try:
                yield connection

            except Exception as exc:
                await connection.rollback()
                raise exc

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception('Database session maker is not set')

        session = self._sessionmaker()
        try:
            yield session

        except Exception as exc:
            await session.rollback()
            raise exc

        finally:
            await session.close()


session_manager = DatabaseSessionManager(settings.DATABASE_URL)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with session_manager.session() as session:
        yield session
