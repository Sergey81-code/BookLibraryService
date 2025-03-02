from fastapi import Depends
from api.v1.books.repository import BookRepository
from api.v1.books.service import BookService
from db.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session():
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session


def get_book_service(repo: BookRepository = Depends()):
    return BookService(repo)