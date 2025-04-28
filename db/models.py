import datetime
import enum
import uuid
from sqlalchemy import Enum, ForeignKey, MetaData, Table
from sqlalchemy.dialects.postgresql import UUID
from uuid_extensions import uuid7
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from typing import Annotated
from db.session import sync_engine
from utils.book_conditions import BookConditions
from utils.book_statuses import BookStatuses

metadata = MetaData()

# Определите таблицу users без модели
users_table = Table("users", metadata, autoload_with=sync_engine)

Base = declarative_base()

uuid_pk = Annotated[uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)]




class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid_pk]
    name: Mapped[str]
    description: Mapped[str | None]
    url: Mapped[str | None]
    year: Mapped[int]
    totalAmount: Mapped[int]
    borrowedAmount: Mapped[int]

    authors: Mapped[list["Author"]] = relationship(
        "Author", 
        secondary="book_authors",
        back_populates="books",
        lazy="selectin"
    )


class Book_copy(Base):
    __tablename__ = "book_copies"

    id: Mapped[uuid_pk]
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Book.id, ondelete="CASCADE"))
    status: Mapped[BookStatuses] = mapped_column(Enum(BookStatuses, name='book_statuses_enum'))
    condition: Mapped[BookConditions] = mapped_column(Enum(BookConditions, name='book_conditions_enum'))
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey(users_table.c.user_id, use_alter=True, ondelete="SET NULL"))


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[uuid_pk]
    name: Mapped[str]
    birthday: Mapped[datetime.date | None]
    deathday: Mapped[datetime.date | None]

    books: Mapped[list[Book]] = relationship(
        Book,
        secondary="book_authors",
        back_populates="authors",
        lazy="selectin"
    )


class BookAuthor(Base):
    __tablename__ = "book_authors"

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Author.id, ondelete="CASCADE"),
        primary_key=True
        )
    
    book_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Book.id, ondelete="CASCADE"),
        primary_key=True
        )