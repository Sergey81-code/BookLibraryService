from uuid import UUID
from sqlalchemy.exc import IntegrityError

from api.core.base_service import BaseService
from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.authors.schemas import AuthorCreate, AuthorUpdate, Book
from api.v1.books.repository import BookRepository
from db.models import Author
from db.models import Book as Book_db

class AuthorService(BaseService):

    def __init__(self, repo: AuthorRepository, book_repo: BookRepository| None = None):
        self.book_repo = book_repo
        super().__init__(repo)
        

    async def _check_author_exist(self, authorName: str,) -> bool:
        existing_author = await self.repo.get_author_by_name(authorName)
        if existing_author:
            return True
        return False
    

    async def _get_only_existing_books(self, books: list[Book] | list[dict[str, str]]) -> list[Book_db] | list:
        received_books_ids = []
        for book in books:
            if isinstance(book, dict):
                received_books_ids.append(books["id"])
            else:
                received_books_ids.append(book.id)
        return await self.book_repo.get_all(
            [lambda model: model.id.in_(received_books_ids)],
        )

    async def create_author_orm_obj(
            self, 
            body_with_author_info: AuthorCreate, 
        ):
        if body_with_author_info.books:
            body_with_author_info.books = await self._get_only_existing_books(body_with_author_info.books)
        return Author(**body_with_author_info.model_dump(exclude_none=True))
    

    async def create_author_in_database(self, author: Author) -> Author:
        try:
            if await self._check_author_exist(author.name):
                AppExceptions.bad_request_exception(f"Author with name {author.name} already exists.")
            return await self.repo.add(author)
        except IntegrityError:
            AppExceptions.service_unavailable_exception("Database error.")

    async def get_author_by_id(self, author_id: UUID) -> Author:
        author = await self.repo.get_by_id(author_id)
        if not author:
            AppExceptions.not_found_exception(f"Author with id {author_id} not found")
        return author


    async def update_books_in_author(self, author: Author, books: list[Book]) -> Author:
        books: list[Book_db] = await self._get_only_existing_objects(books)

        existing_book_ids = {book.id for book in author.books}
        new_book_ids = {book.id for book in books}

        books_to_add = [book for book in books if book not in existing_book_ids]
        books_to_remove = [book for book in author.books if book not in new_book_ids]

        return await self.repo.update_books_in_author(author, books_to_add, books_to_remove)


    async def update_author(self, author: Author, body_with_updated_author_params: AuthorUpdate) -> Author:
        try:
            if author.name != body_with_updated_author_params.name and\
                await self._check_author_exist(body_with_updated_author_params.name):
                AppExceptions.bad_request_exception(f"Author with name {body_with_updated_author_params.name} already registered")
            updated_authors_params = body_with_updated_author_params.model_dump(exclude_none=True)
            if not updated_authors_params:
                AppExceptions.validation_exception(
                    "At least one parameter for book update info should be proveded"
                )
            if books := updated_authors_params.get('books'):
                author = await self.update_books_in_author(author, books)
            updated_authors_params.pop('books', None)
            return await self.repo.update_obj(author, updated_authors_params)
        except IntegrityError:
            AppExceptions.service_unavailable_exception("Database error.")

    async def delete_author_by_id(self, author_id: UUID) -> UUID:
        await self.repo.get_by_id(author_id)
        return await self.repo.delete_by_id(author_id)
    

