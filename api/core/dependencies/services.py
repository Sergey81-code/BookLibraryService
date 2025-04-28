from fastapi import Depends
from api.core.dependencies.repositories import get_author_repository, get_book_copy_repository, get_book_repository
from api.v1.authors.repository import AuthorRepository
from api.v1.authors.service import AuthorService
from api.v1.book_copy.repository import BookCopyRepository
from api.v1.book_copy.service import BookCopyService
from api.v1.books.repository import BookRepository
from api.v1.books.service import BookService


async def get_book_service(
        repo: BookRepository = Depends(get_book_repository),
        auth_repo: AuthorRepository = Depends(get_author_repository),
    ):
    return BookService(repo, auth_repo)

async def get_author_service(
        repo: AuthorRepository = Depends(get_author_repository),
        book_repo: BookRepository = Depends(get_book_repository),
    ):
    return AuthorService(repo, book_repo)

async def get_book_copy_service(
        repo: BookCopyRepository = Depends(get_book_copy_repository),
        book_repo: BookRepository = Depends(get_book_repository),
        auth_repo: AuthorRepository = Depends(get_author_repository),
    ):
    return BookCopyService(repo, book_repo, auth_repo)

