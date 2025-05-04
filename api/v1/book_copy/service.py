from sqlite3 import IntegrityError
from typing import Any
from uuid import UUID
from api.core.base_service import BaseService
from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.book_copy.repository import BookCopyRepository
from api.v1.book_copy.schemas import BookCopy, ShowBookCopy, UpdateBookCopy
from api.v1.books.repository import BookRepository
from db.models import Book, Book_copy


class BookCopyService(BaseService):
    
    def __init__(self, repo: BookCopyRepository, book_repo: BookRepository, auth_repo: AuthorRepository):
        super().__init__(repo)
        self.book_repo = book_repo
        self.auth_repo = auth_repo

    async def _check_book_exist(self, book_id: UUID) -> bool:
        book = await self.book_repo.get_by_id(book_id)
        if book:
            return True
        return False

    async def _create_book_copy_orm_model(self, book_copy: BookCopy) -> Book_copy:
        if not await self._check_book_exist(book_copy.book_id):
            AppExceptions.not_found_exception(f"Book with id {book_copy.book_id} not found")
        return Book_copy(**book_copy.model_dump())
    

    
    async def create_show_book_copy(self, book_copy: Book_copy) -> ShowBookCopy:
        book: Book = await self.book_repo.get_by_id(book_copy.book_id)
        author_names: list[str] = [author.name for author in book.authors]
        return ShowBookCopy(
            id=book_copy.id,
            book_id=book_copy.book_id,
            status=book_copy.status,
            condition=book_copy.condition,
            user_id=book_copy.user_id,
            borrowed_date=book_copy.borrowed_date,
            book_name=book.name,
            description=book.description,
            url=book.url,
            year=book.year,
            author_names=author_names
        )
    
    async def create_book_copies(self, book_copies: list[BookCopy]):
        book_orm_model_copies = [await self._create_book_copy_orm_model(book) for book in book_copies]
        try:
            creating_books_copies_in_database: list[Book_copy] = await self.repo.create_book_copies(book_orm_model_copies)
        except IntegrityError:
            AppExceptions.service_unavailable_exception(f"Database error.")
        return [await self.create_show_book_copy(book) for book in creating_books_copies_in_database]


    async def get_book_copy_by_id(self, book_copy_id: UUID) -> ShowBookCopy:
        book_copy = await self.repo.get_by_id(book_copy_id)
        if book_copy is None:
            AppExceptions.not_found_exception(f"Book copy with id {book_copy_id} not found")
        return await self.create_show_book_copy(book_copy)
    

    async def get_book_copies_by_book_id(self, book_id: UUID, user_id) -> list[ShowBookCopy] | list:
        filters = []
        if book_id:
            filters.append(lambda model: model.book_id == book_id)
        if user_id:
            filters.append(lambda model: model.user_id == user_id)
        book_copies = await self.repo.get_all(filters)
        return [await self.create_show_book_copy(book_copy) for book_copy in book_copies]
    

    async def _get_only_book_copies_with_existed_book(
            self, book_copies: list[dict[str, Any]] | list[BookCopy]
        ) -> list[dict[str, Any]]:
        existed_books = set()
        valid_book_copies = []

        for book_copy in book_copies:
            book_id = (
                book_copy.get("book_id")
                if isinstance(book_copy, dict)
                else getattr(book_copy, "book_id", None)
            )

            if book_id and book_id not in existed_books:
                book = await self.book_repo.get_by_id(book_id)
                if not book:
                    continue

                existed_books.add(book_id)

            valid_book_copies.append(book_copy)
                    
        return valid_book_copies

                




    async def update_book_copies(self, book_copies: list[UpdateBookCopy]) -> list[ShowBookCopy] | list:
        book_copies_updated = []
        for book_copy in book_copies:
            book_copy_dumped = book_copy.model_dump(exclude_none=True)
            if len(book_copy_dumped) > 1:
                book_copies_updated.append(book_copy_dumped)
        
        book_copies_updated = await self._get_only_book_copies_with_existed_book(book_copies_updated)
        updated_book_copies = await self.repo.update_book_copies(book_copies_updated)
        return [await self.create_show_book_copy(book_copy) for book_copy in updated_book_copies]



    async def delete_book_copies(self, book_copy_ids: list[UUID]) -> list[UUID]:
        return await self.repo.delete_objects_by_ids(book_copy_ids)