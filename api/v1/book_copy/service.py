from sqlite3 import IntegrityError
from api.core.base_service import BaseService
from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.book_copy.repository import BookCopyRepository
from api.v1.book_copy.schemas import BookCopy, ShowBookCopy
from api.v1.books.repository import BookRepository
from db.models import Book, Book_copy


class BookCopyService(BaseService):
    
    def __init__(self, repo: BookCopyRepository, book_repo: BookRepository, auth_repo: AuthorRepository):
        super().__init__(repo)
        self.book_repo = book_repo
        self.auth_repo = auth_repo

    async def _create_book_copy_orm_model(self, book: BookCopy) -> Book_copy:
        return Book_copy(**book.model_dump())
    
    async def create_show_book_copy(self, book_copy: BookCopy | Book_copy) -> ShowBookCopy:
        book: Book = await self.book_repo.get_by_id(book_copy.book_id)
        author_names: list[str] = [author.name for author in book.authors]
        return ShowBookCopy(
            book_id=book_copy.book_id,
            status=book_copy.status,
            condition=book_copy.condition,
            user_id=book_copy.user_id,
            book_name=book.name,
            description=book.description,
            url=book.url,
            year=book.year,
            author_names=author_names
        )
    
    async def create_book_copies(self, book_copies: list[BookCopy]):
        book_orm_model_copies = [await self.create_book_copy_orm_model(book) for book in book_copies]
        try:
            creating_books_copies_in_database: list[Book_copy] = await self.repo.create_book_copies(book_orm_model_copies)
        except IntegrityError:
            AppExceptions.service_unavailable_exception(f"Database error.")
        return [await self.create_show_book_copy(book) for book in creating_books_copies_in_database]
