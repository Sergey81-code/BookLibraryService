from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.dependencies import get_author_service, get_session
from api.v1.authors.schemas import AuthorCreate, AuthorUpdate, ShowAuthor
from api.v1.authors.service import AuthorService

author_router = APIRouter()

@author_router.get('/', response_model=ShowAuthor)
async def get_author(
        author_id: UUID,
        session: AsyncSession = Depends(get_session),
        author_service: AuthorService = Depends(get_author_service),
    ):
    return await author_service.get_author_by_id(author_id, session)


@author_router.post('/', response_model=ShowAuthor)
async def create_author(
        body: AuthorCreate,
        session: AsyncSession = Depends(get_session),
        author_service: AuthorService = Depends(get_author_service),
    ):
    author = await author_service.create_author_orm_obj(body, session)
    return await author_service.create_author_in_database(author, session)


@author_router.patch('/', response_model=ShowAuthor)
async def update_authors(
        author_id: UUID,
        body: AuthorUpdate,
        session: AsyncSession = Depends(get_session),
        author_service: AuthorService = Depends(get_author_service),
    ):
    author = await author_service.get_author_by_id(author_id, session)
    return await author_service.update_author(author, body, session)