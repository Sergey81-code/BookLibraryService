from sqlalchemy import insert, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Book_copy


class BookCopyRepository(BaseRepository[Book_copy]):
    
    def __init__(self, session: AsyncSession):
        super().__init__(Book_copy, session)

    async def get_book_copy_by_name(self, name: str,) -> Book_copy | None:
        result = await self.session.execute(select(self.model).where(self.model.name == name).limit(1))
        book_copy_row = result.first()
        return book_copy_row if book_copy_row else None
    
    async def create_book_copies(self, book_copies: list[Book_copy]) -> list[Book_copy]:
        values = [
            {
                column.key: getattr(book, column.key)
                for column in inspect(book).mapper.column_attr
            }
            for book in book_copies
        ]
        stmt = insert(Book_copy).values(values).returning(Book_copy)
        result = await self.session.execute(stmt)
        return result.scalars().all()
