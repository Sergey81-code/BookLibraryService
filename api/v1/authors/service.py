from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.authors.schemas import AuthorCreate, AuthorUpdate, Book
from api.v1.books.repository import BookRepository
from db.models import Author

book_repo = BookRepository()

class AuthorService:

    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def _get_only_existing_books(
            self, 
            books: list[Book], 
            session: AsyncSession
        ) -> list[Book] | list:
        existing_books = await book_repo.get_all(session)
        existing_books_id = [book.id for book in existing_books]
        return [book for book in books if book.id in existing_books_id]
    

    async def _check_author_exist(self, authorName: str, session: AsyncSession) -> bool:
        existing_author = await self.repo.get_author_by_name(authorName, session)
        if existing_author:
            return True
        return False
    

    async def create_author_orm_obj(
            self, 
            body_with_author_info: AuthorCreate, 
            session: AsyncSession
        ):
        if body_with_author_info.books:
            body_with_author_info.books = await self._get_only_existing_books(body_with_author_info.books, session)
        return Author(**body_with_author_info.model_dump(exclude_none=True))
    

    async def create_author_in_database(self, author: Author, session: AsyncSession) -> Author:
        try:
            if await self._check_author_exist(author.name, session):
                AppExceptions.bad_request_exception(f"Book with name {author.name} already exists.")
            return await self.repo.add(session, author)
        except IntegrityError:
            AppExceptions.service_unavailable_exception("Database error.")

    async def get_author_by_id(self, author_id: UUID, session: AsyncSession) -> Author:
        author = await self.repo.get_by_id(session, author_id)
        if author:
            AppExceptions.not_found_exception(f"Author with id {author_id} not found")
        return author


    async def update_books_in_authors(self, author: Author, books: list[Book], session: AsyncSession) -> Author:
        books = self._get_only_existing_books(books)
        book_ids = [book.id for book in books]
        books_from_db = await book_repo.get_all(session, [lambda model: model.id.in_(book_ids)])
        books_to_add = set(books_from_db) - author.books
        books_to_remove = author.books - set(books_from_db)

        return await self.repo.update_books_in_authors(session, author, books_to_add, books_to_remove)


    async def update_author(self, author: Author, body_with_updated_author_params: AuthorUpdate, session: AsyncSession) -> Author:
        try:
            if author.name != body_with_updated_author_params.name and\
                await self._check_author_exist(body_with_updated_author_params.name):
                AppExceptions.bad_request_exception(f"Author with name {body_with_updated_author_params.name} already registered")
            updated_authors_params = body_with_updated_author_params.model_dump(exclude_none=True)
            if not updated_authors_params:
                AppExceptions.validation_exception(
                    "At least one parameter for book update info should be proveded"
                )
            if updated_authors_params['books']:
                author = await self.update_books_in_authors()
            del updated_authors_params['books']
            return await self.repo.update_obj(session, author, updated_authors_params)
        except IntegrityError:
            AppExceptions.service_unavailable_exception("Database error.")
    

