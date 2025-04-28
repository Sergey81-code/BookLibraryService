from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.authors.repository import AuthorRepository
from api.v1.book_copy.repository import BookCopyRepository
from api.v1.books.repository import BookRepository
from db.session import get_session


async def get_book_repository(session: AsyncSession = Depends(get_session)):
    return BookRepository(session)

async def get_author_repository(session: AsyncSession = Depends(get_session)):
    return AuthorRepository(session)

async def get_book_copy_repository(session: AsyncSession = Depends(get_session)):
    return BookCopyRepository(session)

