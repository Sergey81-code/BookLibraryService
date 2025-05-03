import enum
from typing import Any
from sqlalchemy import case, cast, insert, inspect, select, update
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
                for column in inspect(book).mapper.column_attrs
                if column.key != "id"
            }
            for book in book_copies
        ]
        stmt = insert(Book_copy).values(values).returning(Book_copy)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().all()


    async def update_book_copies(self, book_copies: list[dict[str, Any]]) -> list[Book_copy]:
        if not book_copies:
            return []
       
        ids = [book_copy["id"] for book_copy in book_copies]

        field_cases = {}
        for book_copy in book_copies:
            for field, value in book_copy.items():
                if field == "id":
                    continue

                # if isinstance(value, enum.StrEnum):
                #     value = value.value

                if field not in field_cases:
                    field_cases[field] = []
                field_cases[field].append((book_copy["id"], value))

        
        values = {
            field: case(
                {id_: cast(val, getattr(Book_copy.__table__.c, field).type) for id_, val in id_val_pairs},
                value=Book_copy.id,
                else_=getattr(Book_copy, field)
            )
            for field, id_val_pairs in field_cases.items()
        }

        stmt = (
            update(Book_copy)
            .where(Book_copy.id.in_(ids))
            .values(**values)
            .returning(Book_copy)
            .execution_options(synchronize_session=False)           
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.scalars().all()
