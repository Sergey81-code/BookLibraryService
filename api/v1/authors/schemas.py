import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, field_validator, model_validator

from api.core.exceptions import AppExceptions

class TundeModel(BaseModel):
    class ConfigDict:
        from_attributes = True


class Book(BaseModel):
    id: UUID

class ShowBook(TundeModel):
    id: UUID
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    year: int
    totalAmount: int
    borrowedAmount: int


class ShowAuthor(TundeModel):
    id: UUID
    name: str
    birthday: Optional[datetime.date] = None
    deathday: Optional[datetime.date] = None

    books: list[ShowBook] = []


class AuthorCreate(BaseModel):
    name: str
    birthday: Optional[datetime.date] = None
    deathday: Optional[datetime.date] = None

    books: list[Book] = []

    @model_validator(mode="before")
    def capitalize_name(cls, values):
        if "name" in values:
            values['name'] = values['name'].capitalize()
        return values
    
    @field_validator("deathday")
    def validate_borrowed_amount(cls, value, info):
        birthday = info.data.get('birthday')
        if birthday is not None and value <= birthday:
            AppExceptions.bad_request_exception("Birthday cannot be greater than deathday")
        return value
    

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[datetime.date] = None
    deathday: Optional[datetime.date] = None

    books: list[Book] = []

    @model_validator(mode="before")
    def capitalize_name(cls, values):
        if "name" in values:
            values['name'] = values['name'].capitalize()
        return values
    
    @field_validator("deathday")
    def validate_borrowed_amount(cls, value, info):
        birthday = info.data.get('birthday')
        if birthday is not None and value <= birthday:
            AppExceptions.bad_request_exception("Birthday cannot be greater than deathday")
        return value