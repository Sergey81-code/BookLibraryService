from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository
from db.models import Author, Book


class AuthorRepository(BaseRepository[Author]):
    def __init__(self, session: AsyncSession):
        super().__init__(Author, session)

    async def get_author_by_name(self, authorName: str) -> Author | None:
        result = await self.session.execute(select(self.model).where(self.model.name == authorName).limit(1))
        book_row = result.first()
        return book_row[0] if book_row else None
    

    async def update_books_in_author(
            self, 
            author: Author, 
            books_to_add: list[Book], 
            books_to_remove: list[Book]
        ) -> Author:

        for book in books_to_add:
            author.books.append(book)
        
        for book in books_to_remove:
            author.books.remove(book)

        await self.session.commit()
        await self.session.refresh(author)
        return author