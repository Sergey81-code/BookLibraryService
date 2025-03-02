import asyncio
import os
from typing import Any, AsyncGenerator
import asyncpg
import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from api.core.config import get_settings
from api.core.dependencies import get_session
from main import app

settings = get_settings()

CLEAN_TABLES = [
    "books",
    "authors",
    "book_copies",
    "book_authors",
]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    alembic_ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)

    command.upgrade(alembic_cfg, "heads")
    yield
    command.downgrade(alembic_cfg, "base")

@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session

@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test.begin():
        for table_for_cleaning in CLEAN_TABLES:
            await async_session_test.execute(
                sqlalchemy.text(f"""TRUNCATE TABLE {table_for_cleaning};""")
            )

async def _get_test_session():
    try:
        test_engine = create_async_engine(
            settings.TEST_DATABASE_URL, future=True, echo=True
        )
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession 
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[TestClient, Any]:
    """
    Create a new FastApi TestClient that uses the 'db_session' fixture to override
    the 'get_session' dependency that is injected into routers.
    """

    app.dependency_overrides[get_session] = _get_test_session
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    await pool.close()


