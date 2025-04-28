from functools import partial
from fastapi import APIRouter, Depends

from api.core.dependencies.role_required import role_required
from api.core.dependencies.services import get_book_copy_service
from api.v1.book_copy.schemas import BookCopy, ShowBookCopy
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


@book_copy_router.patch("/")
async def update_book_copies():
    pass


@book_copy_router.get("/", response_model=list[ShowBookCopy])
async def get_book_copies():
    pass


@book_copy_router.delete("/")
async def delete_book_copies():
    pass


@book_copy_router.post('/borrow/')
async def borrow_book():
    pass


@book_copy_router.post('/return')
async def return_book():
    pass