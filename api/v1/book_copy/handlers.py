from functools import partial
from uuid import UUID
from fastapi import APIRouter, Depends

from api.core.dependencies.role_required import role_required
from api.core.dependencies.services import get_book_copy_service
from api.v1.book_copy.schemas import BookCopy, ShowBookCopy, UpdateBookCopy
from api.v1.book_copy.service import BookCopyService
from utils.roles import PortalRole


book_copy_router = APIRouter()


@book_copy_router.post(
        "/", 
        response_model=list[ShowBookCopy], 
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])]
    )
async def create_book_copies(
    book_copies: list[BookCopy],
    book_copy_service: BookCopyService = Depends(get_book_copy_service),
):
    return await book_copy_service.create_book_copies(book_copies)


@book_copy_router.patch("/", response_model=list[ShowBookCopy])
async def update_book_copies(
    book_copies: list[UpdateBookCopy],
    book_copy_service: BookCopyService = Depends(get_book_copy_service),
):
    return await book_copy_service.update_book_copies(book_copies)


@book_copy_router.get("/{book_copy_id}")
async def get_book_copy(
    book_copy_id: UUID,
    book_copy_service: BookCopyService = Depends(get_book_copy_service),
):
    return await book_copy_service.get_book_copy_by_id(book_copy_id)


@book_copy_router.get("/all/")
async def get_book_copid_by_book_id(
    book_id: UUID | None = None,
    user_id: UUID | None = None,
    book_copy_service: BookCopyService = Depends(get_book_copy_service),
) -> list[ShowBookCopy] | list:
    return await book_copy_service.get_book_copies_by_book_id(book_id, user_id)


@book_copy_router.delete("/")
async def delete_book_copies(
    book_copy_ids: list[UUID],
    book_copy_service: BookCopyService = Depends(get_book_copy_service),
) -> list[UUID]:
    return await book_copy_service.delete_book_copies(book_copy_ids)


@book_copy_router.post('/borrow/')
async def borrow_book():
    pass


@book_copy_router.post('/return')
async def return_book():
    pass