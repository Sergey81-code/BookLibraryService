from uuid import UUID
from functools import partial

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.dependencies import get_book_service, get_session, role_required
from api.v1.books.schemas import BookCreate, BookUpdate, ShowBook
from api.v1.books.service import BookService
from utils.roles import PortalRole

book_router = APIRouter()



@book_router.post('/', response_model=ShowBook)
async def add_book(
        body: BookCreate, 
        session: AsyncSession = Depends(get_session),
        book_service: BookService = Depends(get_book_service),
        _ = Depends(partial(role_required, 
                        [PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])
                    ),
    ) -> ShowBook:
    book = await book_service.create_book_orm_obj(body, session)
    return await book_service.create_book_in_database(book, session)
    


@book_router.get('/', response_model=ShowBook)
async def get_book(
        book_id: UUID,
        session: AsyncSession = Depends(get_session),
        book_service: BookService = Depends(get_book_service),
    ) -> ShowBook:
    return await book_service.get_book_by_id(book_id, session)


@book_router.patch('/', response_model=ShowBook)
async def update_book_by_id(
        book_id: UUID,
        body: BookUpdate,
        session: AsyncSession = Depends(get_session),
        book_service: BookService = Depends(get_book_service),
        _ = Depends(partial(role_required, 
                    [PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])
                ),
    ) -> ShowBook: 
    book = await book_service.get_book_by_id(book_id, session)
    return await book_service.update_book(book, body, session)



@book_router.delete('/')
async def delete_books(
        book_ids: list[UUID],
        session: AsyncSession = Depends(get_session),
        book_service: BookService = Depends(get_book_service),
        _ = Depends(partial(role_required, 
                [PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])
            ),
    ) -> list[UUID]:
    return await book_service.delete_books_by_ids(book_ids, session)

@book_router.post('/borrow/')
async def borrow_book():
    pass

@book_router.post('/return')
async def return_book():
    pass

