from uuid import UUID
from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.books.repository import BookRepository
from api.v1.books.schemas import Author, BookCreate, BookUpdate
from db.models import Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

auth_repo = AuthorRepository()

class BookService:

    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def _get_only_existing_authors(self, authors: list[Author], session: AsyncSession) -> list:
        existing_authors = await auth_repo.get_all(session)
        existing_authors_ids = [author.id for author in existing_authors]
        return [author for author in authors if author.id in existing_authors_ids]
    
    async def _check_book_exist(self, bookName: str, session: AsyncSession) -> bool:
        existing_book = await self.repo.get_book_by_name(session, bookName)
        if existing_book:
            return True
        return False


    async def create_book_orm_obj(self, body_with_book_info: BookCreate, session: AsyncSession) -> Book:
        body_with_book_info.authors = await self._get_only_existing_authors(body_with_book_info.authors, session)
        return Book(**body_with_book_info.model_dump(exclude_none=True))


    async def create_book_in_database(self, book: Book, session: AsyncSession):
        try:
            if await self._check_book_exist(book.name, session):
                AppExceptions.bad_request_exception(f"Book with name {book.name} already exists.")
            return await self.repo.add(session, book)
        except IntegrityError:
            AppExceptions.service_unavailable_exception(f"Database error.")
    

    async def get_book_by_id(self, book_id: UUID, session: AsyncSession) -> Book:
        book = await self.repo.get_by_id(session, book_id)
        if not book:
            AppExceptions.not_found_exception(f"Book with id {book_id} not found")
        return book
    

    async def delete_book_by_id(self, book_id: UUID, session: AsyncSession) -> Book:
        await self.get_book_by_id(book_id, session)
        return await self.repo.delete_by_id(session, book_id)
    
    async def update_authors_into_book(self, book: Book, authors: list[Author], session: AsyncSession) -> Book:
        authors = await self._get_only_existing_authors(authors)
        authors_from_db = []
        for author in authors:
            author_obj = await auth_repo.get_by_id(author.id)
            authors_from_db.append(author_obj)
        
        authors_to_add = set(authors_from_db) - book.authors
        authors_to_remove = book.authors - set(authors_from_db)

        return await self.repo.update_authors_into_book(session, book, authors_to_add, authors_to_remove)
    

    async def update_book(self, book: Book, body_with_updated_book_params: BookUpdate, session: AsyncSession) -> Book:
        try:
            if not await self._check_book_exist(book.name, session):
                AppExceptions.not_found_exception(f"Book with id {book.id} not found")
            if book.name != body_with_updated_book_params.name and await self._check_book_exist(body_with_updated_book_params.name, session):
                AppExceptions.bad_request_exception(f"Book name {body_with_updated_book_params.name} already taken")
            updated_book_params = body_with_updated_book_params.model_dump(exclude_none=True)
            if not updated_book_params:
                AppExceptions.validation_exception(
                    "At least one parameter for book update info should be proveded"
                )
            if updated_book_params['authors']:
                book = self.update_authors_into_book(book, updated_book_params['authors'], session)
            del updated_book_params['authors']
            return await self.repo.update_obj(session, book, updated_book_params)
        except IntegrityError:
            AppExceptions.service_unavailable_exception(f"Database error.")
