from fastapi import Depends
from api.v1.authors.repository import AuthorRepository
from api.v1.authors.service import AuthorService
from api.v1.books.repository import BookRepository
from api.v1.books.service import BookService
from db.session import async_session

async def get_session():
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session

async def get_book_service(repo: BookRepository = Depends()):
    return BookService(repo)

async def get_author_service(repo: AuthorRepository = Depends()):
    return AuthorService(repo)