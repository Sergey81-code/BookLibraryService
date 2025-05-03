from uuid import UUID
from functools import partial

from fastapi import APIRouter, Depends

from api.core.dependencies.role_required import role_required
from api.core.dependencies.services import get_book_service
from api.v1.books.schemas import BookCreate, BookUpdate, ShowBook
from api.v1.books.service import BookService
from utils.roles import PortalRole

book_router = APIRouter()



@book_router.post(
        '/', 
        response_model=ShowBook, 
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])]
    )
async def add_book(
        body: BookCreate, 
        book_service: BookService = Depends(get_book_service),
    ) -> ShowBook:
    book = await book_service.create_book_orm_obj(body)
    return await book_service.create_book_in_database(book)
    


@book_router.get('/{book_id}', response_model=ShowBook)
async def get_book(
        book_id: UUID,
        book_service: BookService = Depends(get_book_service),
    ) -> ShowBook:
    return await book_service.get_book_by_id(book_id)


@book_router.patch(
        '/', 
        response_model=ShowBook,
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])]
    )
async def update_book_by_id(
        book_id: UUID,
        body: BookUpdate,
        book_service: BookService = Depends(get_book_service),
    ) -> ShowBook: 
    book = await book_service.get_book_by_id(book_id)
    return await book_service.update_book(book, body)



@book_router.delete(
        '/',
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])],
    )
async def delete_books(
        book_ids: list[UUID],
        book_service: BookService = Depends(get_book_service),
    ) -> list[UUID]:
    return await book_service.delete_books_by_ids(book_ids)


@book_router.get('/', response_model=ShowBook)
async def get_book_by_name(
    book_name: str,
    book_service: BookService = Depends(get_book_service),
) -> ShowBook:
    return await book_service.get_book_by_name(book_name)