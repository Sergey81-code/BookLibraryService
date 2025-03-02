from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Author, Book



class BookRepository(BaseRepository[Book]):
    def __init__(self):
        super().__init__(Book)

    async def get_book_by_name(self, session: AsyncSession, name: str) -> Book | None:
        result = await session.execute(select(self.model).where(self.model.name == name).limit(1))
        book_row = result.first()
        return book_row[0] if book_row else None
    
    async def update_authors_into_book(
            self, 
            session: AsyncSession, 
            book: Book, 
            authors_to_add: list[Author], 
            authors_to_remove: list[Author]
        ) -> Book:
        for author in authors_to_add:
            book.authors.append(author)
        
        for author in authors_to_remove:
            book.authors.remove(author)

        await session.commit()
        await session.refresh(book)
        return book