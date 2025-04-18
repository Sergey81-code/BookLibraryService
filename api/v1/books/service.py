from uuid import UUID
from api.core.base_service import BaseService
from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.books.repository import BookRepository
from api.v1.books.schemas import Author, BookCreate, BookUpdate
from db.models import Book
from db.models import Author as Author_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

auth_repo = AuthorRepository()

class BookService(BaseService[Book]):

    def __init__(self, repo: BookRepository):
        super().__init__(repo)

    async def _get_only_existing_authors(self, authors: list[Author] | list[dict[str, str]], session: AsyncSession) -> list[Author_db] | list:
        received_author_ids = []
        for author in authors:
            if isinstance(author, dict):
                received_author_ids.append(author["id"])
            else:
                received_author_ids.append(author.id)
        return await auth_repo.get_all(
            session, 
            [lambda model: model.id.in_(received_author_ids)],
        )
    
    
    async def _check_book_exist(self, bookName: str, session: AsyncSession) -> bool:
        existing_book = await self.repo.get_book_by_name(session, bookName)
        if existing_book:
            return True
        return False


    async def create_book_orm_obj(self, body_with_book_info: BookCreate, session: AsyncSession) -> Book:
        authors = await self._get_only_existing_authors(body_with_book_info.authors, session)
        if authors:
            return Book(**body_with_book_info.model_dump(exclude={"authors"}, exclude_none=True), authors=authors)
        AppExceptions.bad_request_exception("At least one valid author must be provided to create a book.")


    async def create_book_in_database(self, book: Book, session: AsyncSession) -> Book:
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
    

    async def delete_books_by_ids(self, book_ids: list[UUID], session: AsyncSession) -> Book:
        if not book_ids:
            AppExceptions.validation_exception("List of book IDs cannot be empty")
        books = await self._get_only_existing_objects(book_ids, session)
        if not books:
            AppExceptions.not_found_exception("The books with your IDs are not found.")
        existing_books_ids = [book.id for book in books]
        return await self.repo.delete_objects_by_ids(session, existing_books_ids)
    
    async def update_authors_into_book(self, book: Book, authors: list[Author] | list[dict[str, str]], session: AsyncSession) -> Book:
        authors: list[Author_db] = await self._get_only_existing_authors(authors, session)

        existing_authors_id = {author.id for author in book.authors}
        new_authors_id = {author.id for author in authors}

        authors_to_add = [author for author in authors if author.id not in existing_authors_id]
        authors_to_remove = [author for author in book.authors if author.id not in new_authors_id]

        return await self.repo.update_authors_into_book(session, book, authors_to_add, authors_to_remove)
    

    async def update_book(self, book: Book, body_with_updated_book_params: BookUpdate, session: AsyncSession) -> Book:
        try:
            if book.name != body_with_updated_book_params.name and await self._check_book_exist(body_with_updated_book_params.name, session):
                AppExceptions.bad_request_exception(f"Book name {body_with_updated_book_params.name} already taken")
            
            updated_book_params = body_with_updated_book_params.model_dump(exclude_none=True)

            if authors := updated_book_params.get('authors'):
                book = await self.update_authors_into_book(book, authors, session)
                if not book.authors:
                    AppExceptions.bad_request_exception("At least one valid author must be provided to create a book.")

            updated_book_params.pop("authors", None)

            if not updated_book_params:
                AppExceptions.validation_exception(
                    "At least one parameter for book update info should be proveded"
                )

            return await self.repo.update_obj(session, book, updated_book_params)
        
        except IntegrityError:
            AppExceptions.service_unavailable_exception(f"Database error.")
