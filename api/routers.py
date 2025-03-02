from fastapi import APIRouter

from api.v1.books.handlers import book_router
from api.v1.authors.handlers import author_router


router = APIRouter()

api_v1 = APIRouter(prefix="/v1")

api_v1.include_router(book_router, prefix="/books", tags=["books"])
api_v1.include_router(author_router, prefix="/authors", tags=["authors"])


router.include_router(api_v1)
