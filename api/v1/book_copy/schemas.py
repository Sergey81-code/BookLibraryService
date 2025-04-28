from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from utils.book_conditions import BookConditions
from utils.book_statuses import BookStatuses


class TundeModel(BaseModel):
    class Config:
        from_attributes = True


class BookCopy(BaseModel):
    book_id: UUID
    status: BookStatuses
    condition: BookConditions
    user_id: UUID



class ShowBookCopy(TundeModel):
    book_id: UUID
    book_name: str
    status: BookStatuses
    condition: BookConditions
    user_id: UUID
    description: Optional[str] = None
    url: Optional[str] = None
    year: int
    author_names: list[str]


class CreateBookCopies(BaseModel):
    book_copies: list[BookCopy]


class Delete_book_copies(BaseModel):
    book_copies_id: list[UUID]


