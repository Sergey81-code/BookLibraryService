from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Author, Book


class AuthorRepository(BaseRepository[Author]):
    def __init__(self):
        super().__init__(Author)

    async def get_author_by_name(self, authorName: str, session: AsyncSession) -> Author | None:
        result = await session.execute(select(self.model).where(self.model.name == authorName).limit(1))
        book_row = result.first()
        return book_row[0] if book_row else None
    

    async def update_books_in_authors(
            self, 
            session: AsyncSession,
            author: Author, 
            books_to_add: list[Book], 
            books_to_remove: list[Book]
        ) -> Author:

        for book in books_to_add:
            author.books.append()
        
        for book in books_to_remove:
            author.books.remove(book)

        await session.commit()
        await session.refresh(author)
        return author