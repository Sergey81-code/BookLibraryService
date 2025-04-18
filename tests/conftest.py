import asyncio
import os
from typing import Any, AsyncGenerator, Callable
from uuid import UUID
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
from tests.sql_queries import QUERY_TO_DELETE_PROCESSES_PG, QUERY_TO_UNBLOCKING_PROCCESS_PG
from tests.testDAL import TestDAL


settings = get_settings()

CLEAN_TABLES = [
    "book_authors",
    "books",
    "authors",
    "book_copies",
]

VERSION_URL = "/v1"
BOOK_URL = "/books"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    alembic_ini_path = os.path.join(os.getcwd(), "tests", "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)

    command.upgrade(alembic_cfg, "head")
    yield

@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session

@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    query = "TRUNCATE TABLE "+ ",".join(CLEAN_TABLES) + " CASCADE;"
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(sqlalchemy.text(QUERY_TO_UNBLOCKING_PROCCESS_PG))
            await session.execute(sqlalchemy.text(QUERY_TO_DELETE_PROCESSES_PG))
            await session.execute(
                sqlalchemy.text(query)
            )

async def _get_test_session():
    test_engine = create_async_engine(
        settings.TEST_DATABASE_URL, future=True, echo=True
    )
    test_async_session = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession 
    )
    async with test_async_session() as session:
        yield session


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


@pytest.fixture
async def get_book_from_database(asyncpg_pool: asyncpg.Pool) -> Callable[[UUID], asyncpg.Record | None]:
    async def get_book_from_database_by_id(obj_id: UUID) -> asyncpg.Record | None:
        dal = TestDAL(asyncpg_pool)
        book = await dal.get_obj_from_database_by_id("books", obj_id)
        if book:
            book = dict(book)
            book_authors = await dal.get_all(
                "book_authors", 
                [lambda tablename: f"{tablename}.book_id = '{book["id"]}'"],
            )
            book['authors'] = book_authors 
        return book
    
    return get_book_from_database_by_id


@pytest.fixture
async def create_author_in_database(asyncpg_pool: asyncpg.Pool) -> Callable[[dict[str | list[dict[str]]]], str]:
    async def create_author_in_database(author_info) -> str:
        dal = TestDAL(asyncpg_pool)
        books: list[dict[str]] = author_info.pop("books", [])
        author_id = await dal.create_object_in_database("authors", author_info)
        for book in books:
            await dal.create_object_in_database("book_authors", {"book_id": book["id"], "author_id": author_id})
        return author_id
    return create_author_in_database


@pytest.fixture
async def create_book_in_database(asyncpg_pool: asyncpg.Pool) -> Callable[[dict[str | list[dict[str]]]], str]:
    async def create_book_in_database(book_info) -> str:
        dal = TestDAL(asyncpg_pool)
        authors: list[dict[str]] = book_info.pop("authors", [])
        book_id = await dal.create_object_in_database("books", book_info)
        for author in authors:
            await dal.create_object_in_database(
                "book_authors", 
                {
                    "book_id": book_id, 
                    "author_id": author["id"]
                },
                "book_id"
            )
        return book_id
    return create_book_in_database
